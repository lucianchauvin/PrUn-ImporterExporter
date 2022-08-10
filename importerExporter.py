import requests, sys

prices = requests.get("https://rest.fnar.net/csv/prices").text

prices = [x.split(",") for x in [y for y in prices.split("\r\n")]]
headers = prices.pop(0)
tickers = [x[0] for x in prices]


#Takes two commodity exchanges and returns the best item to buy at the first one and sell at the other one.
def best(inCur, outCur):
    best = []
    for x in prices:
        try:
            if(int(x[headers.index(outCur + "-BidPrice")]) - int(x[headers.index(inCur + "-AskPrice")]) >= 0):
                best.append((x[0], (int(x[headers.index(outCur + "-BidPrice")]
                                        ) - int(x[headers.index(inCur + "-AskPrice")])) * min([int(x[headers.index(outCur + "-BidAmt")]), int(x[headers.index(inCur + "-AskAmt")])]), (int(x[headers.index(outCur + "-BidPrice")]
                                                                                                                                                                                           ) - int(x[headers.index(inCur + "-AskPrice")])), min([int(x[headers.index(outCur + "-BidAmt")]), int(x[headers.index(inCur + "-AskAmt")])])))
        except:
            pass
    return best


currencies = ["AI1", "CI2", "CI1", "IC1", "NC2", "NC1"]

with open('out.txt', 'w') as f:
    f.write("InCur -> OutCur [(Material, Net Profit, Profit per unit sold, The max amount of units that can be bought at InCur and sold at OutCur)] \n")
    yeah = ("", "",0,0,0)
    for x in currencies:
        for y in currencies:
            if x != y:
                b = best(x, y)
                f.write(x + " -> " + y + "      " + str(b) + "\n")
                for z in b:
                    if z[1] > yeah[2]:
                        yeah = (x + " -> " + y, z[0], z[1], z[2], z[3])
    f.write("\nBest deal in the entire universe:\n" + str(yeah))