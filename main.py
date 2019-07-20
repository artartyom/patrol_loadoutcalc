import windowClass as wnd
import items

itemlist = items.load_items("items.tsv")

main=wnd.Window("Calculator")

for item in itemlist:
    main.add_multibutton(item)

main.render()