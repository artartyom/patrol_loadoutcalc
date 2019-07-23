import windowClass as wnd
import pandas as pd

itemlist = pd.read_csv("items.tsv", sep="\t")
main=wnd.Window("Calculator", itemlist)