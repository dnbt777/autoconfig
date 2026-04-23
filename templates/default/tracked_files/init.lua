-- init.lua


vim.o.number = true
vim.o.relativenumber = true
vim.o.termguicolors=true



-- BOOTSTRAP lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("todo_extras")

-- PLUGIN SETUP with lazy.nvim
require("lazy").setup({
  -- Zig syntax plugin
  {
    "ziglang/zig.vim",
    ft = "zig", -- optional: load only for .zig files
  },
  {
      'Julian/lean.nvim',
      event = { 'BufReadPre *.lean', 'BufNewFile *.lean' },

      dependencies = {
        'neovim/nvim-lspconfig',
        'nvim-lua/plenary.nvim',

        -- optional dependencies:

        -- a completion engine
        --    hrsh7th/nvim-cmp or Saghen/blink.cmp are popular choices

        -- 'nvim-telescope/telescope.nvim', -- for 2 Lean-specific pickers
        -- 'andymass/vim-matchup',          -- for enhanced % motion behavior
        -- 'andrewradev/switch.vim',        -- for switch support
        -- 'tomtom/tcomment_vim',           -- for commenting
      },

      ---@type lean.Config
      opts = { -- see below for full configuration options
        mappings = true,
      }
    },
    {
    'nvim-telescope/telescope.nvim', tag = 'v0.2.0',
     dependencies = { 'nvim-lua/plenary.nvim' }
    }

})

-- EDITOR OPTIONS
vim.o.showcmd = true
vim.o.tabstop = 4
vim.o.shiftwidth = 4
vim.o.expandtab = true



-- Keybinds
vim.keymap.set('n', '<leader>f', require('telescope.builtin').find_files) -- telescope find_files

