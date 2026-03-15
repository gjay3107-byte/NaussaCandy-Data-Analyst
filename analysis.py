import pandas as pd
df = pd.read_csv("data.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y")
df = df[df["Ship Date"] >= df["Order Date"]]
df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
factory_map = {
"Wonka Bar - Nutty Crunch Surprise":"Lot's O' Nuts",
"Wonka Bar - Fudge Mallows":"Lot's O' Nuts",
"Wonka Bar -Scrumdiddlyumptious":"Lot's O' Nuts",
"Wonka Bar - Milk Chocolate":"Wicked Choccy's",
"Wonka Bar - Triple Dazzle Caramel":"Wicked Choccy's",
"Laffy Taffy":"Sugar Shack",
"SweeTARTS":"Sugar Shack",
"Nerds":"Sugar Shack",
"Fun Dip":"Sugar Shack",
"Fizzy Lifting Drinks":"Sugar Shack",
"Everlasting Gobstopper":"Secret Factory",
"Hair Toffee":"The Other Factory",
"Lickable Wallpaper":"Secret Factory",
"Wonka Gum":"Secret Factory",
"Kazookles":"The Other Factory"
}
df["Factory"] = df["Product Name"].map(factory_map)
df["Route"] = df["Factory"] + " → " + df["State/Province"]
route_stats = df.groupby("Route").agg(
    Shipments=("Order ID","count"),
    Avg_Lead_Time=("Lead Time","mean"),
    Lead_Time_STD=("Lead Time","std")
).reset_index()
ship_mode_stats = df.groupby("Ship Mode").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Total_Shipments=("Order ID","count")
).reset_index()
state_stats = df.groupby("State/Province").agg(
    Avg_Lead_Time=("Lead Time","mean"),
    Shipments=("Order ID","count")
).reset_index()
threshold = 5
df["Delayed"] = df["Lead Time"] > threshold
delay_stats = df.groupby("Route")["Delayed"].mean().reset_index()
df.to_csv("processed_data.csv", index=False)
route_stats.to_csv("route_stats.csv", index=False)
ship_mode_stats.to_csv("ship_mode_stats.csv", index=False)
state_stats.to_csv("state_stats.csv", index=False)
print("Data Processing Completed")