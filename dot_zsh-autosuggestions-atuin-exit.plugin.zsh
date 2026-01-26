#!/usr/bin/env zsh

# zsh-autosuggestions-atuin-exit
# Colors zsh-autosuggestions suggestions based on atuin's last exit status.

typeset -g ZSH_ATUIN_AUTOSUGGEST_STATUS_PLUGIN_LOADED=1

# Default colors (edit these to taste)
typeset -g _ATUIN_AUTOSUGGEST_SUCCESS_STYLE='fg=#5fa980'
typeset -g _ATUIN_AUTOSUGGEST_FAILURE_STYLE='fg=#a06a6a'

# Cache the last queried suggestion per prompt.
typeset -g _ATUIN_AUTOSUGGEST_LAST_CMD=''
typeset -g _ATUIN_AUTOSUGGEST_LAST_EXIT='unknown'

# "Return values" written by functions (avoid $(...) so we don't lose state).
typeset -g _ATUIN_AUTOSUGGEST_EXIT_CODE='unknown'
typeset -g _ATUIN_AUTOSUGGEST_NEXT_STYLE=''

_atuin_autosuggest_status__have_atuin() {
  emulate -L zsh
  (( $+commands[atuin] || $+functions[atuin] ))
}

_atuin_autosuggest_status__force_global_filter_mode() {
  emulate -L zsh

  # Off by default.
  # Set ZSH_ATUIN_AUTOSUGGEST_FORCE_GLOBAL_FILTER=1 to enable.
  [[ "${ZSH_ATUIN_AUTOSUGGEST_FORCE_GLOBAL_FILTER-}" == 1 ]]
}

_atuin_autosuggest_status__atuin_find_exit() {
  emulate -L zsh

  local cmd=$1
  local cwd=${2-}
  local out line

  [[ -n $cmd ]] || return 1
  [[ $cmd != *$'\n'* && $cmd != *$'\r'* ]] || return 1

  local -a args
  args=(atuin search --include-duplicates --limit 20 --search-mode prefix --format '{command}\t{exit}')

  if _atuin_autosuggest_status__force_global_filter_mode; then
    args+=(--filter-mode global)
  fi

  if [[ -n $cwd ]]; then
    args+=(--cwd "$cwd")
  fi

  args+=(-- "$cmd")
  out=$("${args[@]}" 2>/dev/null) || return 1

  # Pick the newest exact match from the results.
  while IFS=$'\n' read -r line; do
    if [[ -n "$line" && "$line" == "$cmd"$'\t'* ]]; then
      print -r -- "${line#*$'\t'}"
      return 0
    fi
  done <<< "$out"

  return 1
}

_atuin_autosuggest_status__atuin_last_exit() {
  emulate -L zsh

  local cmd=$1
  local cwd=${2-}
  local exit_code

  # If the command was ever run in this directory, prefer that status.
  if [[ -n $cwd ]]; then
    exit_code=$(_atuin_autosuggest_status__atuin_find_exit "$cmd" "$cwd")
    if [[ -n $exit_code ]]; then
      print -r -- "$exit_code"
      return 0
    fi
  fi

  exit_code=$(_atuin_autosuggest_status__atuin_find_exit "$cmd")
  [[ -n $exit_code ]] || return 1
  print -r -- "$exit_code"
}

_atuin_autosuggest_status__exit_for_command() {
  emulate -L zsh

  local cmd=$1
  _ATUIN_AUTOSUGGEST_EXIT_CODE='unknown'
  [[ -n $cmd ]] || return 0

  if ! _atuin_autosuggest_status__have_atuin; then
    return 0
  fi

  if [[ "$cmd" == "$_ATUIN_AUTOSUGGEST_LAST_CMD" ]]; then
    _ATUIN_AUTOSUGGEST_EXIT_CODE="$_ATUIN_AUTOSUGGEST_LAST_EXIT"
    return 0
  fi

  local exit_code
  exit_code=$(_atuin_autosuggest_status__atuin_last_exit "$cmd" "$PWD")
  [[ -n $exit_code ]] || exit_code=unknown
  _ATUIN_AUTOSUGGEST_LAST_CMD="$cmd"
  _ATUIN_AUTOSUGGEST_LAST_EXIT="$exit_code"
  _ATUIN_AUTOSUGGEST_EXIT_CODE="$exit_code"
}

_atuin_autosuggest_status__style_for_suggestion() {
  emulate -L zsh

  local suggestion=$1
  local exit_code

  _ATUIN_AUTOSUGGEST_NEXT_STYLE="$ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE"

  _atuin_autosuggest_status__exit_for_command "$suggestion"
  exit_code="$_ATUIN_AUTOSUGGEST_EXIT_CODE"

  if [[ $exit_code == <-> ]]; then
    if (( exit_code == 0 )); then
      _ATUIN_AUTOSUGGEST_NEXT_STYLE="$_ATUIN_AUTOSUGGEST_SUCCESS_STYLE"
    elif (( exit_code > 0 )); then
      _ATUIN_AUTOSUGGEST_NEXT_STYLE="$_ATUIN_AUTOSUGGEST_FAILURE_STYLE"
    fi
    return 0
  fi
}

_atuin_autosuggest_status__install() {
  emulate -L zsh

  (( $+functions[_zsh_autosuggest_highlight_apply] )) || return 0
  (( $+functions[_atuin_autosuggest_status__orig_highlight_apply] )) && return 0

  functions[_atuin_autosuggest_status__orig_highlight_apply]="$functions[_zsh_autosuggest_highlight_apply]"

  _zsh_autosuggest_highlight_apply() {
    emulate -L zsh

    local orig=$ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE
    if (( $#POSTDISPLAY )); then
      _atuin_autosuggest_status__style_for_suggestion "$BUFFER$POSTDISPLAY"
      ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="$_ATUIN_AUTOSUGGEST_NEXT_STYLE"
    fi

    _atuin_autosuggest_status__orig_highlight_apply "$@"
    ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE=$orig
  }
}

_atuin_autosuggest_status__precmd() {
  _ATUIN_AUTOSUGGEST_LAST_CMD=''
  _ATUIN_AUTOSUGGEST_LAST_EXIT='unknown'
  _ATUIN_AUTOSUGGEST_EXIT_CODE='unknown'
  _ATUIN_AUTOSUGGEST_NEXT_STYLE=''
}

if (( $+precmd_functions )); then
  (( ! ${precmd_functions[(Ie)_atuin_autosuggest_status__precmd]} )) && precmd_functions+=(_atuin_autosuggest_status__precmd)
  precmd_functions+=(_atuin_autosuggest_status__install)
fi

_atuin_autosuggest_status__install
