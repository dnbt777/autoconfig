--------------------------------------------------------------------------------
-- CONFIGURATION – extend this table to add/change statuses
local STATUS = {
  DONE = { char = 'x', color = '#00ff00', bg = nil },
  WIP  = { char = 'c', color = '#ffff00', bg = nil },
  TODO = { char = 'v', color = '#ff0000', bg = nil },
}
-- (The key → the text that appears in brackets: DONE, WIP, etc.)

--------------------------------------------------------------------------------
-- Internal plumbing ===========================================================
local ns   = vim.api.nvim_create_namespace('todo_done')
local aug  = vim.api.nvim_create_augroup('TodoAutoRedraw', { clear = true })
local enabled = false

-- colors ----------------------------------------------------------------------
for key, cfg in pairs(STATUS) do
  vim.api.nvim_set_hl(0, 'Todo' .. key, { fg = cfg.color, bg = cfg.bg, bold = true })
end

-- strip “ (STATUS)” at EOL only if it is one of the known ones
local function strip_status(line)
  local head, st = line:match('^(.-) %((%u+)%)%s*$')
  if st and STATUS[st] then                -- known status
    return head, st
  end
  return line, nil
end

-- main highlighting engine ----------------------------------------------------
local function redraw(bufnr)
  vim.api.nvim_buf_clear_namespace(bufnr, ns, 0, -1)
  if not enabled then return end

  local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
  for lnum, ln in ipairs(lines) do
    local _, st = strip_status(ln)
    if st then
      local hlg = 'Todo' .. st
      vim.api.nvim_buf_set_extmark(bufnr, ns, lnum - 1, 0, {
        end_line = lnum - 1,
        end_col = #ln,
        hl_group = hlg,
        priority = 100,
      })
    end
  end
end

-- macros ----------------------------------------------------------------------
local function toggle_macros(set)
  for key, meta in pairs(STATUS) do
    local lhs = '@' .. meta.char
    if set then
      -- Factory to properly capture 'key' in closure per iteration
      local function make_rhs(k)
        return function() require('todo_extras').toggle_macro(k) end
      end
      local rhs = make_rhs(key)
      vim.keymap.set('n', lhs, rhs, { buffer = 0, silent = true })
      vim.keymap.set('x', lhs, rhs, { buffer = 0, silent = true })
    else
      pcall(vim.keymap.del, 'n', lhs, { buffer = 0 })
      pcall(vim.keymap.del, 'x', lhs, { buffer = 0 })
    end
  end
end

-- thin public wrapper for the mapping/command
local M = {}

-- exported action
-- Single action called by both the mapping and the visual maps
function M.toggle_macro(status_key)
  local buf = vim.api.nvim_get_current_buf()

  -- which lines?
  local start_line, end_line
  local mode = vim.fn.mode()
  local is_visual = mode:find('[vV␖]') ~= nil
  if is_visual then
    start_line = vim.fn.line("'<")
    end_line = vim.fn.line("'>")
    -- Exit visual mode immediately BEFORE modifying
    vim.cmd [[normal! \<Esc>]]
  else
    start_line = vim.fn.line('.')
    end_line = start_line
  end

  -- Normalize with temps to correctly handle if start > end (even if rare)
  local min_line = math.min(start_line, end_line)
  local max_line = math.max(start_line, end_line)
  start_line = min_line
  end_line = max_line

  -- skip if invalid range
  if start_line < 1 or end_line < 1 then return end

  -- Fetch all lines in range (0-based indices)
  local start_idx = start_line - 1
  local end_idx = end_line
  local lines = vim.api.nvim_buf_get_lines(buf, start_idx, end_idx, false)

  -- Process each line individually
  local new_lines = {}
  for _, line in ipairs(lines) do
    local base, curr = strip_status(line)
    local new_text
    if curr == status_key then
      new_text = base  -- remove
    else
      new_text = base .. ' (' .. status_key .. ')'  -- add/replace
    end
    table.insert(new_lines, new_text)
  end

  -- Set the entire range at once (one modification, efficient)
  vim.api.nvim_buf_set_lines(buf, start_idx, end_idx, false, new_lines)
end

-- Public user command ---------------------------------------------------------
vim.api.nvim_create_user_command('TODO', function(opts)
  enabled = not opts.bang
  local buf = vim.api.nvim_get_current_buf()
  redraw(buf)
  toggle_macros(enabled)
end, { bang = true, desc = 'Toggle todo highlighting & @x/@c/@v macros' })

-- autocommands to keep highlighting live
vim.api.nvim_create_autocmd({'BufWinEnter','TextChanged','TextChangedI'}, {
  group = aug,
  pattern = '*',
  callback = function(ev)
    if enabled then redraw(ev.buf) end
  end,
})

--------------------------------------------------------------------------------
-- Auto-load when placed in ~/.config/nvim/lua/todo_extras.lua
return M  -- Lua requires return
