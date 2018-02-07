" ------------------
" To edit remote files, use :e scp://latte.ca/~/weblog/tech/


" ------------------
augroup mkd
  autocmd BufRead *.mkd  set ai formatoptions=tcroqn2 comments=n:>
  autocmd BufRead *.md  set ai formatoptions=tcroqn2 comments=n:>
  autocmd BufRead *.md~  set ai formatoptions=tcroqn2 comments=n:>
  autocmd BufRead *.mkd set spell
  autocmd BufRead *.md set spell
  autocmd BufRead *.md~ set spell
augroup END

py import sys;sys.path.append("/Users/bwinton/.vim/python")
py import pyblock
py import reviewboard
augroup py
  autocmd BufNewFile,BufRead *.py compiler python
  autocmd FileType python runtime! autoload/pythoncomplete.vim
  autocmd FileType python set omnifunc=pythoncomplete#Complete

  " Watch out for trailing newlines in any python code
  autocmd BufNewFile,BufRead *.py match Error /\s\+$/

  map ( :python pyblock.find(forward = 0)
  map ) :python pyblock.find()

  imap <c-space> <c-x><c-o>
augroup END


" ------------------
" From https://github.com/hallettj/jslint.vim
filetype plugin on
let g:JSLintHighlightErrorLine = 0


" ------------------
" From lmorchard!

map <leader>s :ConqueTermTab zsh

" ------------------
" From http://blog.sontek.net/2008/05/11/python-with-a-modular-ide-vim/

" Use 'gf' to go to a file from an import line.
python << EOF
import os
import sys
import vim
for p in sys.path:
    if p!="" and os.path.isdir(p):
        vim.command(r"set path+=%s" % (p.replace(" ", r"\ ")))
EOF

augroup py

  " Extra syntax highlighting
  autocmd BufNewFile,BufRead *.py match Error /^\s*def\s\+\w\+(.*)\s*$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*class\s\+\w\+(.*)\s*$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*for\s.*[^:]$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*except\s*$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*finally\s*$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*try\s*$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*else\s*$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*else\s*[^:].*/
  autocmd BufNewFile,BufRead *.py match Error /^\s*if\s.*[^\:]$/
  autocmd BufNewFile,BufRead *.py match Error /^\s*except\s.*[^\:]$/
  autocmd BufNewFile,BufRead *.py match Error /[;]$/

  " Let :make compile python programs
  " And we can use :cn/:cp to move forwards/backwards in the error list.
  autocmd BufRead *.py set makeprg=python\ -c\ \"import\ py_compile,sys;\ sys.stderr=sys.stdout;\ py_compile.compile(r'%')\"
  autocmd BufRead *.py set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m

  " Select a method/class and execute it by <c-h>
  python << EOL
from urllib import urlopen
import vim

def EvaluateCurrentRange():
  eval(compile('\n'.join(vim.current.range),'','exec'),globals())


licenses = {
  "cpp": "c",
  "css": "c",
  "html": "html",
  "idl": "c",
  "javascript": "c",
  "python": "sh",
  "xhtml": "html",
  "xml": "html",
}

def AddMozillaLicense():
  # Get the current filetype.
  x = vim.eval("&ft")
  url = "http://www.mozilla.org/MPL/boilerplate-1.1/mpl-tri-license-" + licenses.get(x, "txt")
  data = urlopen(url).readlines()
  vim.current.buffer[0:0] = data
  vim.command(":1")
  vim.command("/________")
  vim.command("n")

EOL
  autocmd FileType python map <C-h> :py EvaluateCurrentRange()
augroup END

" ------------------
" From http://items.sjbach.com/319/configuring-vim-right

let mapleader = ","
set history=1000
set scrolloff=3

map <leader>b :call BlogCheck()<CR>
map <leader>l :py AddMozillaLicense()<CR>

" ------------------
" Map ,f to take the Weekly Status from Things, and massage it for 
" http://benjamin.smedbergs.us/weekly-updates.fcgi/
python << EOL
import vim
def FixupStatusNotes():
  vim.command(r"/^ *$")
  vim.command(r":1,.s/^- \(.*\)$/  <li>\1<\/li>/")
  vim.command(r":.,$s/^- \(.*\)$/<li>\1<\/li>/")
  vim.current.buffer[0:0] = ["<ul><li>Account Provisioner:<ul>"]
  vim.command(r":%s/^ *$/<\/ul><\/li>")
  vim.current.buffer.append("</ul>")
EOL
map <leader>f :py FixupStatusNotes()<CR>

" ------------------
" Use ,- and ,= to make the current line headers in Markdown.
" It actually does it for everything, not just Markdown,
" but there you go, I guess.

augroup mkd
  python << EOL
import vim
def MkdMakeHeader( headerChar ):
  buffer = vim.current.buffer
  row, col = vim.current.window.cursor
  line = vim.current.line
  line = line.decode('UTF-8')
  buffer[row:row] = [headerChar*len(line)]
EOL
  autocmd FileType mkd map <leader>- :py MkdMakeHeader( '-' )
  autocmd FileType mkd map <leader>= :py MkdMakeHeader( '=' )
  autocmd FileType mkd set makeprg=markdown\ %
  autocmd FileType mkd map <leader>m :make
augroup END

augroup xml
  autocmd FileType xml set formatprg=xmllint\ --format\ %
augroup END

augroup nu
  autocmd FileType nu set formatprg=nubile
  autocmd FileType nu set makeprg=nush\ %
  autocmd FileType nu map <leader>m :!nush %
augroup END

" ------------------
" From http://weblog.jamisbuck.org/2008/11/17/vim-follow-up

" Use ack as my grep.
set grepprg=ack\ -H\ --column\ --no-group\ --no-color
set grepformat=%f:%l:%c:%m

" Some indentation settings.
set tabstop=4
set smarttab
set shiftwidth=4
set autoindent
set expandtab
set textwidth=75

" Modified by http://www.perlmonks.org/?node_id=333744
set backspace=start,eol,indent

" Some display settings.
set hlsearch
syntax on

set statusline=%F%m%r%h%w\ %{&ff}\ [0x\%02.2B]%=[%v,%l/%L\ %p%%]
set laststatus=2

" NERD tree toggle key.
map <leader>d :execute 'NERDTreeToggle ' . getcwd()<CR>

function! s:ToggleScratch() 
  if expand('%') == g:ScratchBufferName 
    quit 
  else 
    Sscratch 
  endif 
endfunction 

" Save ,s for insert stack trace.
" map <leader>s :call <SID>ToggleScratch()<CR>

ab #s try {(0)()} catch (e) dump("Stack Trace:\n"+e.stack.replace(/^.*?\n/,'').replace(/(?:\n@:0)?\s+$/m,'').replace(/^\(/gm,'{anonymous}(').split("\n"));

" ------------------
" from http://video.google.com/videoplay?docid=2538831956647446078
" 7 habits for Effective Text Editing 2.0 by Bram Moolenaar.

set incsearch

" Ctrl-N will fill in stuff from earlier in the file!

" ------------------
" Don't do this until we can get mvim to run on Python 2.5
" This is because I can't (well, don't want to) add pyflakes to Python2.3.
" pyfile ~/.vim/python/check.py

" ------------------
" from http://everything101.sourceforge.net/docs/papers/java_and_vim.html
" but modified by http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_gF
" make gf open with the line number, in a new tab.
map gf <C-W>gF

" from
" http://osdir.com/ml/linux.debian.packages.vim.devel/2004-04/msg00002.html
" If we can't find the filename for the gf, then try removing a leading
" "a/" or "b/".  Stupid git diff format.
augroup diff
  set includeexpr=substitute(v:fname,'^[ab]/','','')
  autocmd BufNewFile,BufRead *.diff\|*.patch match Error /^+.\{-}\zs\s\+$/
  autocmd FileType diff match Error /^+.\{-}\zs\s\+$/
augroup END

augroup mozilla
  autocmd BufNewFile,BufRead *.c(pp)?\|*.jsm?\|*.dtd\|*.x[mu]l\|*.py match Error /\s\+$/
  autocmd FileType javascript match Error /\s\+$/
augroup END

" ------------------
colorscheme macvim
set background=dark

" ------------------
" From http://writequit.org/blog/?p=195
if has("gui_running")
  set guioptions-=T       " no toolbar
  set cursorline          " show the cursor line
end
set modelines=0           " no modelines [http://www.guninski.com/vim1.html]
set showmatch             " show matching bracket.

" ------------------
" C-R, " will paste from the kill buffer in insert mode.
"      See also: :help <C-R> for extra cool stuff.<M-Right><D-Right>
"
" ⌘{ and ⌘} will switch between tabs.  Bleah.
"
" C-n and C-p will auto-complete next and previous in insert mode.
"
"
" ,t will use the really cool file opener!  Seriously, use it!!!
"
"
" ⌘⇧F toggles fullscreen.  The options below control it.
" set fuoptions=maxhorz,maxvert
set fuoptions=maxvert,background:Normal

" ,n and ,p will go forward and back in the error/grep list.
map <leader>n :cn<CR>
map <leader>p :cp<CR>

" For use in figuring out what commands I use, when running the custom version.
if has('cmdlog')
  " cmdlogdir:
  "     The directory which will be used to store logs.
  set cmdlogdir=~/.vim/logs/
  " cmdloginsert:
  "     Log text entered in normal mode.
  "     Disabled by default
  " set cmdloginsert
end

" ------------------
" From http://stanford.edu/~jlebar/blog/2010/2/1/Hacking%2C_part_1%3A_Vim.html
set wildmenu
set wildignore=*.o,*.obj,*.bak,*.exe,*.class,*.swp

set softtabstop=4
set shiftwidth=4

" ------------------
" From http://github.com/itfrombit/nuvim
" <C-c>n     :  Reindent Nu file
"
" If you've run "screen -S nush nush", then the following work:
" <C-c><C-c> :  Send current scope or selection to screen
" <C-c>f     :  Send entire file to screen
" <C-c>c     :  Connect to a different screen session

au BufNewFile,BufRead *.nu,*.nujson,Nukefile    setf nu

