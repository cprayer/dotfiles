from colormath.color_conversions import convert_color
from colormath.color_objects import LCHabColor,sRGBColor

def tohex(l,c,h):
  rgb = convert_color(LCHabColor(l,c,h),sRGBColor)
  clamp = sRGBColor(rgb.clamped_rgb_r, rgb.clamped_rgb_g, rgb.clamped_rgb_b)
  return clamp.get_rgb_hex()

def phic(e):
  return 0.61803398875**e*100

def print_airline(name,bg):
  print 'auxfile autoload/airline/themes/%s_%s.vim' % (name, bg)
  print 'let g:airline#themes#%s_%s#palette = {}' % (name, bg)
  print ''
  print 'let s:gry0 = [ "@guigry0", @termgry0 ]'
  print 'let s:gry1 = [ "@guigry1", @termgry1 ]'
  print 'let s:gry3 = [ "@guigry3", @termgry3 ]'
  print 'let s:red_ = [ "@guired_", @termred_ ]'
  print 'let s:gren = [ "@guigren", @termgren ]'
  print 'let s:blue = [ "@guiblue", @termblue ]'
  print ''
  print 'let s:nrm1 = [ s:gry0[0] , s:gry3[0] , s:gry0[1] , s:gry3[1] ]'
  print 'let s:nrm2 = [ s:gry3[0] , s:gry1[0] , s:gry3[1] , s:gry1[1] ]'
  print 'let s:insr = [ s:gry0[0] , s:gren[0] , s:gry0[1] , s:gren[1] ]'
  print 'let s:visl = [ s:gry0[0] , s:blue[0] , s:gry0[1] , s:blue[1] ]'
  print 'let s:rplc = [ s:gry0[0] , s:red_[0] , s:gry0[1] , s:red_[1] ]'
  print 'let s:inac = [ s:gry3[0] , s:gry1[0] , s:gry3[1] , s:gry1[1] ]'
  print ''
  print 'let g:airline#themes#%s_%s#palette.normal =' % (name, bg)
  print '  \ airline#themes#generate_color_map( s:nrm1 , s:nrm2 , s:nrm2 )'
  print ''
  print 'let g:airline#themes#%s_%s#palette.insert =' % (name, bg)
  print '  \ airline#themes#generate_color_map( s:insr , s:nrm2 , s:nrm2 )'
  print ''
  print 'let g:airline#themes#%s_%s#palette.visual =' % (name, bg)
  print '  \ airline#themes#generate_color_map( s:visl , s:nrm2 , s:nrm2 )'
  print ''
  print 'let g:airline#themes#%s_%s#palette.replace =' % (name, bg)
  print '  \ airline#themes#generate_color_map( s:rplc , s:nrm2 , s:nrm2 )'
  print ''
  print 'let g:airline#themes#%s_%s#palette.inactive =' % (name, bg)
  print '  \ airline#themes#generate_color_map( s:inac , s:inac , s:inac )'
  print ''
  print 'if !get(g:, "loaded_ctrlp", 0)'
  print '  finish'
  print 'endif'
  print ''
  print 'let g:airline#themes#%s_%s#palette.ctrlp =' % (name, bg)
  print '  \ airline#extensions#ctrlp#generate_color_map( s:nrm2 , s:nrm1 , s:nrm2 )'
  print 'endauxfile'

def print_lightline(name,bg):
  print 'auxfile autoload/lightline/colorscheme/%s_%s.vim' % (name, bg)
  print 'let s:gry0 = [ "@guigry0", @termgry0 ]'
  print 'let s:gry1 = [ "@guigry1", @termgry1 ]'
  print 'let s:gry3 = [ "@guigry3", @termgry3 ]'
  print 'let s:red_ = [ "@guired_", @termred_ ]'
  print 'let s:mgnt = [ "@guimgnt", @termmgnt ]'
  print 'let s:gren = [ "@guigren", @termgren ]'
  print 'let s:blue = [ "@guiblue", @termblue ]'
  print ''
  print 'let s:p = { "normal" : {} , "inactive": {} , "insert"  : {} ,'
  print '          \ "replace": {} , "visual"  : {} , "tabline" : {} }'
  print ''
  print 'let s:p.normal.left     = [[ s:gry0, s:gry3 ], [ s:gry3, s:gry1 ]]'
  print 'let s:p.normal.middle   = [[ s:gry3, s:gry1 ]]'
  print 'let s:p.normal.right    = [[ s:gry0, s:gry3 ], [ s:gry0, s:gry3 ]]'
  print ''
  print 'let s:p.inactive.left   = copy(s:p.normal.middle)'
  print 'let s:p.inactive.middle = copy(s:p.normal.middle)'
  print 'let s:p.inactive.right  = copy(s:p.normal.middle)'
  print ''
  print 'let s:p.insert.left     = [[ s:gry0, s:gren ]]'
  print 'let s:p.insert.right    = [[ s:gry0, s:gren ], [ s:gry0, s:gren ]]'
  print ''
  print 'let s:p.visual.left     = [[ s:gry0, s:blue ]]'
  print 'let s:p.visual.right    = [[ s:gry0, s:blue ], [ s:gry0, s:blue ]]'
  print ''
  print 'let s:p.replace.left    = [[ s:gry0, s:red_ ]]'
  print 'let s:p.replace.right   = [[ s:gry0, s:red_ ], [ s:gry0, s:red_ ]]'
  print ''
  print 'let s:p.tabline.left    = copy(s:p.normal.middle)'
  print 'let s:p.tabline.tabsel  = [[ s:gry0, s:gren ]]'
  print 'let s:p.tabline.right   = copy(s:p.normal.middle)'
  print ''
  print 'let s:p.normal.error    = [[ s:red_, s:gry0 ]]'
  print 'let s:p.normal.warning  = [[ s:mgnt, s:gry0 ]]'
  print ''
  print 'let g:lightline#colorscheme#%s_%s#palette =' % (name, bg)
  print '  \ lightline#colorscheme#flatten(s:p)'
  print 'endauxfile'

def print_shell(name,bg):
  print 'auxfile shell/%s_%s.sh' % (name, bg)
  print '#!/bin/sh'
  print '# base16-shell (https://github.com/chriskempson/base16-shell)'
  print '# Base16 Shell template by Chris Kempson (http://chriskempson.com)'
  print '# %s_%s scheme by haystackandroid (https://github.com/haystackandroid/stellarized)' % (name, bg)
  print ''
  print 'color00="@guigry0" # Base 00 - Black'
  print 'color01="@guired_" # Base 08 - Red'
  print 'color02="@guigren" # Base 0B - Green'
  print 'color03="@guigold" # Base 0A - Yellow'
  print 'color04="@guiblue" # Base 0D - Blue'
  print 'color05="@guimgnt" # Base 0E - Magenta'
  print 'color06="@guicyan" # Base 0C - Cyan'
  print 'color07="@guigry3" # Base 05 - White'
  print 'color08="@guigry1" # Base 03 - Bright Black'
  print 'color09=$color01 # Base 08 - Bright Red'
  print 'color10=$color02 # Base 0B - Bright Green'
  print 'color11=$color03 # Base 0A - Bright Yellow'
  print 'color12=$color04 # Base 0D - Bright Blue'
  print 'color13=$color05 # Base 0E - Bright Magenta'
  print 'color14=$color06 # Base 0C - Bright Cyan'
  print 'color15="@guigryc" # Base 07 - Bright White'
  print 'color_foreground="@guigry3" # Base 05'
  print 'color_background="@guigry0" # Base 00'
  print ''
  print 'if [ -n "$TMUX" ]; then'
  print "  # Tell tmux to pass the escape sequences through"
  print "  # (Source: http://permalink.gmane.org/gmane.comp.terminal-emulators.tmux.user/1324)"
  print "  put_template() { printf '\033Ptmux;\033\033]4;%d;rgb:%s\033\033\\\033\\' $@; }"
  print "  put_template_var() { printf '\033Ptmux;\033\033]%d;rgb:%s\033\033\\\033\\' $@; }"
  print "  put_template_custom() { printf '\033Ptmux;\033\033]%s%s\033\033\\\033\\' $@; }"
  print 'elif [ "${TERM%%[-.]*}" = "screen" ]; then'
  print "  # GNU screen (screen, screen-256color, screen-256color-bce)"
  print "  put_template() { printf '\033P\033]4;%d;rgb:%s\007\033\\' $@; }"
  print "  put_template_var() { printf '\033P\033]%d;rgb:%s\007\033\\' $@; }"
  print "  put_template_custom() { printf '\033P\033]%s%s\007\033\\' $@; }"
  print 'elif [ "${TERM%%-*}" = "linux" ]; then'
  print '  put_template() { [ $1 -lt 16 ] && printf "\e]P%x%s" $1 $(echo $2 | sed "s/\///g"); }'
  print "  put_template_var() { true; }"
  print "  put_template_custom() { true; }"
  print "else"
  print "  put_template() { printf '\033]4;%d;rgb:%s\033\\' $@; }"
  print "  put_template_var() { printf '\033]%d;rgb:%s\033\\' $@; }"
  print "  put_template_custom() { printf '\033]%s%s\033\\' $@; }"
  print "fi"
  print ''
  print '# 16 color space'
  print 'put_template 0  $color00'
  print 'put_template 1  $color01'
  print 'put_template 2  $color02'
  print 'put_template 3  $color03'
  print 'put_template 4  $color04'
  print 'put_template 5  $color05'
  print 'put_template 6  $color06'
  print 'put_template 7  $color07'
  print 'put_template 8  $color08'
  print 'put_template 9  $color09'
  print 'put_template 10 $color10'
  print 'put_template 11 $color11'
  print 'put_template 12 $color12'
  print 'put_template 13 $color13'
  print 'put_template 14 $color14'
  print 'put_template 15 $color15'
  print ''
  print '# foreground / background / cursor color'
  print 'if [ -n "$ITERM_SESSION_ID" ]; then'
  print '  # iTerm2 proprietary escape codes'
  print '  put_template_custom Pg @guigry3 # foreground'
  print '  put_template_custom Ph @guigry0 # background'
  print '  put_template_custom Pi @guigry3 # bold color'
  print '  put_template_custom Pj @guiblue # selection color'
  print '  put_template_custom Pk @guigry0 # selected text color'
  print '  put_template_custom Pl @guigry3 # cursor'
  print '  put_template_custom Pm @guigry0 # cursor text'
  print 'else'
  print '  put_template_var 10 $color_foreground'
  print '  if [ "$BASE16_SHELL_SET_BACKGROUND" != false ]; then'
  print '    put_template_var 11 $color_background'
  print '    if [ "${TERM%%-*}" = "rxvt" ]; then'
  print '      put_template_var 708 $color_background # internal border (rxvt)'
  print '    fi'
  print '  fi'
  print '  put_template_custom 12 ";7" # cursor (reverse video)'
  print 'fi'
  print ''
  print '# clean up'
  print 'unset -f put_template'
  print 'unset -f put_template_var'
  print 'unset -f put_template_custom'
  print 'unset color00'
  print 'unset color01'
  print 'unset color02'
  print 'unset color03'
  print 'unset color04'
  print 'unset color05'
  print 'unset color06'
  print 'unset color07'
  print 'unset color08'
  print 'unset color09'
  print 'unset color10'
  print 'unset color11'
  print 'unset color12'
  print 'unset color13'
  print 'unset color14'
  print 'unset color15'
  print 'unset color_foreground'
  print 'unset color_background'
  print 'endauxfile'

def print_fish(name,bg):
  print 'auxfile shell/%s_%s.fish' % (name, bg)
  print '# %s_%s fish shell theme by haystackandroid (https://github.com/haystackandroid/stellarized)' % (name, bg)
  print ''
  print'# normal text'
  print'set fish_color_host              @guigry3'
  print'set fish_color_normal            @guigry3'
  print'set fish_pager_color_completion  @guigry3'
  print'set fish_pager_color_description @guigry3'
  print''
  print'# muted text'
  print'set fish_color_autosuggestion    @guigry2'
  print'set fish_color_comment           @guigry2'
  print''
  print'# reverse muted'
  print'set fish_pager_color_progress    @guigry0 --background=@guigry2'
  print''
  print'# underlined text'
  print'set fish_color_valid_path        --underline'
  print''
  print'# highlit text'
  print'set fish_color_match             --background=@guigryp'
  print'set fish_color_search_match      --background=@guigryp'
  print'set fish_color_selection         --background=@guigryp'
  print''
  print'# red errors/warnings'
  print'set fish_color_cancel            @guired_'
  print'set fish_color_cwd_root          @guired_'
  print'set fish_color_error             @guired_'
  print''
  print'# gold special elements'
  print'set fish_color_redirection       @guigold'
  print'set fish_color_escape            @guigold'
  print'set fish_color_operator          @guigold'
  print'set fish_color_end               @guigold'
  print''
  print'# green commands/status'
  print'set fish_color_command           @guigren'
  print'set fish_color_cwd               @guigren'
  print'set fish_color_user              @guigren'
  print''
  print'# cyan parameters'
  print'set fish_color_param             @guicyan'
  print''
  print'# blue quoted strings'
  print'set fish_color_quote             @guiblue'
  print''
  print'# magenta pager name match'
  print'set fish_pager_color_prefix      @guimgnt'
  print 'endauxfile'

hue_bas0 = 067.5
hue_bas1 = 277.5

hue_red_ = 022.5
hue_gold = 082.5
hue_gren = 142.5
hue_cyan = 202.5
hue_blue = 262.5
hue_mgnt = 322.5

cro_ltacnt = phic(1.00)
cro_dkacnt = phic(2.00)

hexgry0_lt = tohex( phic(0.11) , phic(5.00) , hue_bas0 )
hexgry1_lt = tohex( phic(0.26) , phic(4.50) , hue_bas0 )
hexgry2_lt = tohex( phic(1.62) , phic(4.00) , hue_bas1 )
hexgry3_lt = tohex( phic(2.23) , phic(4.00) , hue_bas1 )

hexgry0_dk = tohex( phic(3.95) , phic(5.00) , hue_bas1 )
hexgry1_dk = tohex( phic(3.27) , phic(4.50) , hue_bas1 )
hexgry2_dk = tohex( phic(1.12) , phic(4.00) , hue_bas0 )
hexgry3_dk = tohex( phic(0.69) , phic(4.50) , hue_bas0 )

hexred__lt = tohex( phic(1.57) , cro_ltacnt , hue_red_ )
hexgold_lt = tohex( phic(1.59) , cro_ltacnt , hue_gold )
hexgren_lt = tohex( phic(1.62) , cro_ltacnt , hue_gren )
hexcyan_lt = tohex( phic(1.80) , cro_ltacnt , hue_cyan )
hexblue_lt = tohex( phic(1.76) , cro_ltacnt , hue_blue )
hexmgnt_lt = tohex( phic(1.61) , cro_ltacnt , hue_mgnt )

hexred__dk = tohex( phic(1.11) , cro_dkacnt , hue_red_ )
hexgold_dk = tohex( phic(1.11) , cro_dkacnt , hue_gold )
hexgren_dk = tohex( phic(1.12) , cro_dkacnt , hue_gren )
hexcyan_dk = tohex( phic(1.15) , cro_dkacnt , hue_cyan )
hexblue_dk = tohex( phic(1.15) , cro_dkacnt , hue_blue )
hexmgnt_dk = tohex( phic(1.13) , cro_dkacnt , hue_mgnt )

hexsrch_lt = tohex( phic(0.25) , phic(0.25) , hue_gold )
hexsrch_dk = tohex( phic(1.50) , phic(1.50) , hue_gold )

lum_ltspel = phic(1.50)
cro_ltspel = phic(0.00)
lum_dkspel = phic(0.75)
cro_dkspel = phic(0.75)

hexsprd_lt = tohex( lum_ltspel , cro_ltspel , hue_red_ )
hexspbl_lt = tohex( lum_ltspel , cro_ltspel , hue_blue )
hexspcy_lt = tohex( lum_ltspel , cro_ltspel , hue_cyan )
hexspmg_lt = tohex( lum_ltspel , cro_ltspel , hue_mgnt )

hexsprd_dk = tohex( lum_dkspel , cro_dkspel , hue_red_ )
hexspbl_dk = tohex( lum_dkspel , cro_dkspel , hue_blue )
hexspcy_dk = tohex( lum_dkspel , cro_dkspel , hue_cyan )
hexspmg_dk = tohex( lum_dkspel , cro_dkspel , hue_mgnt )

print 'Author:          haystackandroid'
print 'Maintainer:      haystackandroid'
print 'License:         MIT'
print 'Full name:       stellarized'
print 'Short name:      stellarized'
print 'Terminal Colors: 256'
print ''
print 'Background: light'
print 'Color:      gry0 %s ~' % hexgry0_lt
print 'Color:      gry1 %s ~' % hexgry1_lt
print 'Color:      gry2 %s ~' % hexgry2_lt
print 'Color:      gry3 %s ~' % hexgry3_lt
print 'Color:      gryc %s ~' % hexgry1_dk
print 'Color:      srch %s ~' % hexsrch_lt
print 'Color:      grys %s ~' % hexgry1_dk
print 'Color:      gryp %s ~' % hexgry3_dk
print 'Color:      sprd %s ~' % hexsprd_lt
print 'Color:      spbl %s ~' % hexspbl_lt
print 'Color:      spcy %s ~' % hexspcy_lt
print 'Color:      spmg %s ~' % hexspmg_lt
print 'Color:      red_ %s ~' % hexred__lt
print 'Color:      gold %s ~' % hexgold_lt
print 'Color:      gren %s ~' % hexgren_lt
print 'Color:      cyan %s ~' % hexcyan_lt
print 'Color:      blue %s ~' % hexblue_lt
print 'Color:      mgnt %s ~' % hexmgnt_lt
print 'Include:    _common.colortemplate'
print ''
print_airline('stellarized','light')
print ''
print_lightline('stellarized','light')
print ''
print_shell('stellarized','light')
print ''
print_fish('stellarized','light')
print ''
print 'Background: dark'
print 'Color:      gry0 %s ~' % hexgry0_dk
print 'Color:      gry1 %s ~' % hexgry1_dk
print 'Color:      gry2 %s ~' % hexgry2_dk
print 'Color:      gry3 %s ~' % hexgry3_dk
print 'Color:      gryc %s ~' % hexgry1_lt
print 'Color:      srch %s ~' % hexsrch_dk
print 'Color:      grys %s ~' % hexgry1_lt
print 'Color:      gryp %s ~' % hexgry3_lt
print 'Color:      sprd %s ~' % hexsprd_dk
print 'Color:      spbl %s ~' % hexspbl_dk
print 'Color:      spcy %s ~' % hexspcy_dk
print 'Color:      spmg %s ~' % hexspmg_dk
print 'Color:      red_ %s ~' % hexred__dk
print 'Color:      gold %s ~' % hexgold_dk
print 'Color:      gren %s ~' % hexgren_dk
print 'Color:      cyan %s ~' % hexcyan_dk
print 'Color:      blue %s ~' % hexblue_dk
print 'Color:      mgnt %s ~' % hexmgnt_dk
print 'Include:    _common.colortemplate'
print ''
print_airline('stellarized','dark')
print ''
print_lightline('stellarized','dark')
print ''
print_shell('stellarized','dark')
print ''
print_fish('stellarized','dark')
