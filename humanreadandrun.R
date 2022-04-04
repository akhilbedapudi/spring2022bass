#install.packages("data.table")
library(data.table)
library(readxl)
data=read_excel('MouseInfo2.xlsx')
data=data[,-c(2)]
data=na.omit(data)

#data=transpose(data, keep.names = "col")
#traits=read.csv('AD_DECODEpower.csv')

#removing AD and MCI
indexofremoval=traits$risk_for_ad >1
sum(indexofremoval)
#dim(traits[indexofremoval,])
#traits=traits[-which(indexofremoval),]


# traits$RAVLT_FORGETTING
# traits$genotype
# traits$sex
# traits$age
# traits$Risk
# traits$RAVLT_IMMEDIATE
#traits$RAVLT_PERCENTFORGETTING=abs(traits$RAVLT_FORGETTING)/traits$AVLT_Trial5
# a=which(as.matrix(traits[4, ])==12, arr.ind=T)
# a
#hist(traits$RAVLT_PERCENTFORGETTING)
#traits$RAVLcategorical=traits$RAVLT_PERCENTFORGETTING
## mak eit as a facotor 0.25 low, 0.5 medium low, 0.75 medium , 1 high 
#traits$RAVLcategorical[traits$RAVLcategorical<=0.25]="Low"
#traits$RAVLcategorical[ traits$RAVLcategorical<=0.5 & traits$RAVLcategorical>0.25]="Medlow"
#traits$RAVLcategorical[ traits$RAVLcategorical<=0.75 & traits$RAVLcategorical>0.5]="Med"
#traits$RAVLcategorical[ traits$RAVLcategorical<=1 & traits$RAVLcategorical>0.75]="High"




#listdatanames=as.numeric(substr(data$col, start = 2, stop = 6))
#listtraitnames=traits$MRI
#length(intersect(listdatanames,listtraitnames))
#comonlist=intersect(listdatanames,listtraitnames)
#matrixdata=matrix(0, length(comonlist),(dim(data)[2]+dim(traits)[2]))

#for (i in 1:length(comonlist)) {
 # cat(which(as.numeric(substr(data$col, start = 2, stop = 6))==comonlist[i]),  "\n")
 #indexvol=which(as.numeric(substr(data$col, start = 2, stop = 6))==comonlist[i])
  #indextrait=which(traits$MRI==comonlist[i])

  #a=data[indexvol,]
  #b=traits[indextrait,]
  #length(c(a,b)) 
  #matrixdata[i,]=unlist(c(a,b))
#}
#colnames(matrixdata)=names(c(a,b))

#matrixdata=as.data.frame(matrixdata)

#for (i in 2:dim(data)[2]) {
  #matrixdata[,i]=as.numeric(matrixdata[, i])
#}
#matrixdata$age=as.numeric(matrixdata$age)

library(jmv)









pvalsresults=matrix(NA,(dim(data)[2]-6)  ,3)
rownames(pvalsresults)=names(data)[6:(dim(data)[2]-1)]
colnames(pvalsresults)= c( "Genotype","Treatment" , "Genotype*Treatment")

library(rstatix)
#install.packages('berryFunctions')
library(berryFunctions)

for (i in 1:dim(data[,-c(1:6)])[2] ) {
  tempname = names(data[,-c(1:5)])[i]
  #if (!(i%in% c(23,30,94,108,128,130,138,150,159,189,196,260,274,294)))
  #res.aov <- anova_test(data = data, get(tempname)~Genotype*Treatment, wid = Mouse, within = TimePoint, type=3)
  #A=res.aov$p
  #pvalsresults[i,] = A
#a=ancova( data = data, dep=tempname, factors = vars(genotype, treatment), homo=T, norm=T)
  if(!is.error(anova_test(data = data, get(tempname)~Genotype*Treatment, wid = Mouse, within = TimePoint, type=3))) {
    res.aov1 <- anova_test(data = data, get(tempname)~Genotype*Treatment, wid = Mouse, within = TimePoint, type=3)
    A=res.aov1$p
    pvalsresults[i,] = A
  }
}
pvalsresults=na.omit(pvalsresults)
pvalsresultsadjusted <- pvalsresults[pvalsresults[,1]<=0.05,]


#Error in Anova.III.lm(mod, error, singular.ok = singular.ok, ...) : 
#  there are aliased coefficients in the model
#Note: model has aliased coefficients
#sums of squares computed by model comparison
###### THis error is beacasue recval% and sex are present and teh residual are very close
pvalsresults[pvalsresults[,2]<=0.05,]

pvalsresultsadjusted=pvalsresults

###adjust pvalues Benjamini & Hochberg
for (j in 1:dim(pvalsresultsadjusted)[2]) {
  pvalsresultsadjusted[,j] = p.adjust(pvalsresultsadjusted[,j], "fdr") #Benjamini & Hochberg
}

#Error in p.adjust(pvalsresultscopy[, j], "BH", n = dim(data)[1]) : 
#  n >= lp is not TRUE
#### DUE TO SMALL SAMPLE SIZE THE P-VALUES CANNOT BE CORRECTED
sig = pvalsresultsadjusted[pvalsresultsadjusted[,1]<=0.05,] #Adjusted P-values
library(emmeans)

sig = sig[,1]
posthocT=matrix(NA,length(sig),7)
for (i in 1:length(sig)) {
  tempname=names(sig)[i]
  res.aov <- aov(get(tempname) ~ Treatment, data = data)
  a=tukey_hsd(res.aov)
  posthocT[,1]=sig
  posthocT[,2:7]=a$p.adj
  rownames(posthocT)[i]=tempname
}

colnames(posthocT)=c("fdr","IL","ILI","IS", "LLI", "LS", "LIS")

 