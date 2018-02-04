library(data.table)
library(plotly)
system('/home/misrori/anaconda3/bin/python /home/misrori/R_kodok/steembot_revenu_calculator/get_data.py minnowvotes')

adat <- data.table(fread("tmp.csv"))
adat$datum <- as.Date(adat$timestamp)
adat$timestamp <- as.POSIXct(adat$timestamp)
adat$usd <- ifelse(adat$asset=="SBD", adat$sbd_price*adat$money, adat$money*adat$steem_price)
adat$steempersbd <- adat$steem_price/adat$sbd_price
adat$justsbd <- ifelse(adat$asset=="SBD", adat$money, adat$money*adat$steempersbd)


orankenti <- adat[,list('usd_revenue'=sum(usd), 'crypto_revenue'= sum(justsbd)), by=timestamp]
naponkenti <- adat[,list('usd_revenue'=sum(usd), 'crypto_revenue'= sum(justsbd)), by=datum]


p<-plot_ly(naponkenti, x = ~datum, y = ~usd_revenue, text= ~paste('Daily earning $',usd_revenue))%>%
  add_lines()
p



p<-plot_ly(orankenti, x = ~timestamp, y = ~crypto_revenue, text= ~paste('Daily earning in SBD $',usd_revenue))%>%
  add_lines()
p




p<-plot_ly(naponkenti, x = ~datum, y = ~crypto_revenue, text= ~paste('Daily earning in SBD $',usd_revenue))%>%
  add_lines()
p



p<-plot_ly(orankenti, x = ~timestamp, y = ~usd_revenue, text= ~paste('Daily earning $',usd_revenue))%>%
  add_lines()
p



