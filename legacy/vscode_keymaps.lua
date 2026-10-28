-- For macOs, located inside .config/nvim/lua/user/

local keymap = vim.keymap.set
local opts = { noremap = true, silent = true }

-- remap leader key
keymap("n", "<Space>", "<Nop>", opts)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- open config file
vim.cmd('nmap <leader>c :e ~/.config/nvim/lua/user/vscode_keymaps.lua<cr>')

-- yank to system clipboard
keymap({"n", "v"}, "<leader>y", '"+y', opts)

-- paste from system clipboard
keymap({"n", "v"}, "<leader>p", '"+p', opts)

-- better indent handling
keymap("v", "<", "<gv", opts)
keymap("v", ">", ">gv", opts)

-- move text up and down
-- keymap("v", "J", ":m .+1<CR>==", opts)
-- keymap("v", "K", ":m .-2<CR>==", opts)
keymap("x", "J", ":move '>+1<CR>gv-gv", opts)
keymap("x", "K", ":move '<-2<CR>gv-gv", opts)

-- paste preserves primal yanked piece
keymap("v", "p", '"_dP', opts)

-- removes highlighting after escaping vim search
keymap("n", "<Esc>", "<Esc>:noh<CR>", opts)

-- remap redo
keymap("n", "U", "<C-r>", opts)

-- remap ctrl+o's functionality to an easier combination
keymap({"n", "v"}, "<leader>b", "<Cmd>call <SNR>7_jump(v:count, 'back')<CR>", opts)

-- remap "extended" motions
keymap({"n", "v"}, "H", "0", opts)
keymap({"n", "v"}, "L", "$", opts)
keymap({"n", "v"}, "J", "}", opts)
keymap({"n", "v"}, "K", "{", opts)

-- add an empty line before the cursor
keymap("n", "<leader>o", "O<Esc>", opts)

-- skip folds
vim.cmd('nmap j gj')
vim.cmd('nmap k gk')

-- call vscode commands from neovim
-- general keymaps
keymap({"n", "v"}, "<leader>t", "<cmd>lua require('vscode').action('workbench.action.terminal.toggleTerminal')<CR>")
keymap({"n", "v"}, "<leader>h", "<cmd>lua require('vscode').action('editor.action.showHover')<CR>")
keymap({"n", "v"}, "<leader>a", "<cmd>lua require('vscode').action('editor.action.quickFix')<CR>")
keymap({"n", "v"}, "<leader>sp", "<cmd>lua require('vscode').action('workbench.actions.view.problems')<CR>")
keymap({"n", "v"}, "<leader>cn", "<cmd>lua require('vscode').action('notifications.clearAll')<CR>")
keymap({"n", "v"}, "<leader>f", "<cmd>lua require('vscode').action('workbench.action.quickOpen')<CR>")
keymap({"n", "v"}, "<leader>cp", "<cmd>lua require('vscode').action('workbench.action.showCommands')<CR>")
keymap({"n", "v"}, "<leader>pr", "<cmd>lua require('vscode').action('code-runner.run')<CR>")
keymap({"n", "v"}, "<leader>fd", "<cmd>lua require('vscode').action('editor.action.formatDocument')<CR>")
keymap({"n", "v"}, "<leader>h", "<cmd>lua require('vscode').action('workbench.action.navigateLeft')<CR>")
keymap({"n", "v"}, "<leader>l", "<cmd>lua require('vscode').action('workbench.action.navigateRight')<CR>")
keymap({"n", "v"}, "<leader>k", "<cmd>lua require('vscode').action('workbench.action.navigateUp')<CR>")
keymap({"n", "v"}, "<leader>j", "<cmd>lua require('vscode').action('workbench.action.navigateDown')<CR>")
keymap({"n", "v"}, "<leader>1", "<cmd>lua require('vscode').action('workbench.action.previousEditorInGroup')<CR>")
keymap({"n", "v"}, "<leader>2", "<cmd>lua require('vscode').action('workbench.action.nextEditorInGroup')<CR>")
keymap({"n", "v"}, "<leader>[", "<cmd>lua require('vscode').action('editor.fold')<CR>")
keymap({"n", "v"}, "<leader>]", "<cmd>lua require('vscode').action('editor.unfold')<CR>")
keymap({"n", "v"}, "<leader>r", "<cmd>lua require('vscode').action('editor.action.rename')<CR>")
keymap({"n", "v"}, "<leader>ff", "<cmd>lua require('vscode').action('find-it-faster.findWithinFiles')<CR>")
keymap({"n", "v"}, "<leader>\\", "<cmd>lua require('vscode').action('workbench.action.splitEditor')<CR>")
keymap({"n", "v"}, "<leader>gg", "<cmd>lua require('vscode').action('lazygit-vscode.toggle')<CR>")
