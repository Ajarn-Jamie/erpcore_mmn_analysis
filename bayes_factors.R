library(BayesFactor)

data <- read.csv("erpcore_mean_amp.csv", header=FALSE)

ss = unlist(data[1])
sd = unlist(data[2])
ds = unlist(data[3])

bf_ssVsd = ttestBF(x=ss, y=sd, paired=TRUE)
bf_ssVds = ttestBF(x=ss, y=ds, paired=TRUE)
bf_sdVds = ttestBF(x=sd, y=ds, paired=TRUE)

print("sS vs. sD")
print(bf_ssVsd)
print("sS vs. dS")
print(bf_ssVds)
print("sD vs. dS")
print(bf_sdVds)