# -*- coding: utf-8 -*-
# grove/content/visuals.py
# Stores the ASCII visuals for different locations.

# Using raw strings r"""...""" for multi-line definitions.
# Internal quote sequences that might conflict with string terminators are modified.

location_visuals = {
    'clearing': r"""
          ~~ ~~
         / \./ \
        |  ` '  |
        | (\_/) |
       @(_ o o _)@      _/_
        / `---' \     (/) (_)
    *  (         )      *
  ` "^^`------'`"^^" `'"

Stone Circle in Clearing
""",
    'dark_woods_entrance': r"""
       ,--./,-.
      / #      \
     |          |
      \  #     /    _.--""--._
       `---\'--'   .'          `.
            \     /   O      O   \
             \   |      `.        |
   🌲         \  \       ^       /  🌲
        🌲     \  `. _______ .'  /
                `._'`-------'`_.'
""",
    'deep_woods': r"""
      )  (  ))   (
     /(         )\  )
    ( /  (    )  \ )
    |/    |)   (\ |
    / (|  (    )  | \    ))
 (( (  #   (\   #  ) )) / )
    ) (\ (  )   # / ) ( (
   ( (  ) )\  #  ( / /   ) )
   ) ) ((  #   ) / / (  ( (
  ( ( ( ) ) \#( ( ( ) ) ) )
   ) ) ) ( ( # ) ) ) ( ( (
  ( ( ( ( ) # ) ( ( ( ) ) )
   ) ) ) ) ( ( ( ) ) ) ) (
      ||         ||
     /__\       /__\
""",
    'gentle_slope_base': r"""
                          ,
              `.  '"'.'"` .'
                `.      .'
             "    `-..-'    "
           ."       ``       ".    *
         .'            `.     '. '`"`'""
        /     ,        \    *   '
  *"   /      .;.       \   `" .' )
    `./'.    .'''.   .'"\.'''.' ;`-.   # Adjusted internal quotes
    .'   `---------`  `.   "     "`.`.
   /                      \           `.\
 .'                        `. .'"`'".'"" `.`.'' # Adjusted internal quotes
`-._                       _.-' '' .-.'`.`.'."`.
    `---------------------`     .""       '"" `'.
""",
    'slope_top': r"""
       _.--""--._
     .'          `.     ~ ~ ~
    /   O      O   \   (💧) (💧)
   |      `.        |  ~ ~ ~
   \       ^       /--._.--._.-🌊-._
    `. _______ .'        `._________.'`.
     .`-------'.`.                  `~ .`
    /           `.\                   ~.`
  .'________________`.                  ~ .
~~~~ Valley Below ~~~~~\.     Spring     ./~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~
""",
    'hidden_track_start': r"""
        \       /
 `.      \ .-. /      .'
   `.     \| |/     .'
      \   /| |\   / \
  ~ ~ ~`-( | | )-'~ ~ ~
         `|" "|`
 Bush   / `---' \   Path
 ~~~~~~/         \~~~~~~
      /           \

""",
    'ancient_tree': r"""
          .--""--.
         /        \      *
        |  O    O  |      .'`.
        \    /\    /    .`    `.
        .`--'--'.,   |   .-""-.   |
       / /|....|\ \  '..'      '..'
      | /`------'\ |   ||        ||
      \            /   ||   /\   ||
       '.  `.  .'  `   /'..'  '..'\    🌳
      🌲 `------'      "----------" 🌲
           ||  ||        \\ //
           ||  ||        ( | )
          /__\/__\        \|/
         `'''''`'`       `-' # Replaced internal triple quotes
        Giant Roots    🌲
""",
    'quiet_stream': r"""
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
  (💧)       __/ {__ \            (💧)
   ~ ~ ~ ~ ~ \____ ) ~ ~ ~ ~ ~ ~ ~ ~
     (💧)      ~~~~~ \             ~ ~
     ~ ~ ~ ~ ~ ~ ~ / \~ ~ ~ ~ ~ ~ ~ ~
      ~ ~ ~ ~ ~ ~ |~~~| ~ ~ ~ ~ ~ ~ ~
     ~ ~ ~ ~ ~ ~ /_____\ ~ ~ ~ ~ ~ ~ ~
             __/ {__    \       (💧)
 ~ ~ ~ ~ ~ ~ \____ ) ~ ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~ ~ ~ ~  ~~~~~ ~ ~ ~ ~ ~ ~ ~ ~ ~
""",
    'valley_view': r"""
                _.--""--._              _.-=~-.
       \,._ .'          `.           .'   '. \_.''.'. , ./ __  # Corrected internal quotes
   \ ._.' /   O      O   \        _{        }_(\.--''.'/^./ - \/ - # Corrected internal quotes
`.`  \  |      `.        |      .' ).      ( ( (\  .--./___./ . /_,./
 `.'~|~ \       ^       / ~~^--{              }--"^---'//___./----._.-"
    .~'.'`.`._ _______ .'`.~    {     V A L L E Y    } ~ ~ ^~ .'..'. .'~~~ # Corrected internal quotes
  .'` .~' .'`-------'."' `.~    '. (\_________/) / ~ ~ .,_,_,.'~ ."'. ."~ # Corrected internal quotes
 ~  .' ,.'`         `.'`. `. ~    "._       _." .'`. ~.''~~~''. .-.. ."~~ # Corrected internal quotes
_..-" .' `.      .'`.   `..'."-._ .~ `'-----'`.' ". `./.'.' . ./ '.' `.`".'` # Corrected internal quotes & removed backticks near . .
."'. .'    `~~~~`    `. . ''. ~ `' . ''. ''. '' `-..-''. ." . '. .''. ."`.`  # Corrected internal quotes
 ''.` ''. ''~~''      `".`.`. .' ."`.'.'. .' ". ''.~~ ." `. ."~~ ." ~~.''.` # Corrected internal quotes
 ''~.'' `.` ~~ `". .'-- ''.``. .'`. ." `. ."~.''.`.'". `. ." ." ".`         # Corrected internal quotes
""", # Previous line 13 modified significantly to simplify problematic quote structures
    'stream_bend': r"""
          _______ Rock _________
       .''`                  `''.
     //       _.--""--._       \\
    ((      .'          `.      ))
     \\    /   O      O   \    // --- Stream Flow --->>>
     ((   |      `.        |   ))
      \\  \       ^       /  // ~~~ ~ ~ ~ ~ ~~~
   ~~~ \\  `. _______ .'  // ~~~ ~ (💧) ~ ~~~
   ~ ~ (( ~~ `-------' ~~ )) ~ ~ ~ ~ ~ ~~~ ~~~
  ~ ~~~~ \\___________// ~~~~~~~~~ ~~~ ~ ~~~
 ~ ~ ~ ~ ~~~~~~~~~~~~~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
"""
}

print("[visuals.py] Loaded.")