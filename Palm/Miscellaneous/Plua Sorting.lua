-- Plua Sorting.lua

x0,y0,x1,y1=20,20,140,140
larg=5 
 n=20
datr={}
dats={}
cmps = 0
swaps = 0

function colour(i)
  return i*2/3 + 127
end

function gendatr()
local i,x
   for i=1,20,1 do
    datr[i] = random(115) + 5
    dats[i] = datr[i]
   end
end

function resetdatr()
local i,x
   for i=1,20,1 do
    datr[i] = dats[i]
   end
end

srttbl={}
functbl={}

function lt(i,j)
  local r
  cmps = cmps + 1
  drawbox(i,16711680)
  drawbox(j,16711680)
  psleep(0,50)
  r=datr[i]<datr[j]
  drawbox(i,colour(datr[i]))
  drawbox(j,colour(datr[j]))
  return r
end

function lte(i,j)
local r
  r = lt(i,j)
  if not r then
    r = (datr[i] == datr[j])
  end
  return r
end

function swap(i, j)
  swaps = swaps + 1
  drawbox(i,0)
  drawbox(j,0)
  datr[i],datr[j]= datr[j],datr[i] 
  drawbox(i,65280)
  drawbox(j,65280)
  psleep(0,100)
  drawbox(i,colour(datr[i]))
  drawbox(j,colour(datr[j]))
end

-- Sort Funcs.
dofile("memo:Sort Simple Funcs.lua")
dofile("memo:Sort Complex Funcs.lua")

function drawbox(i,clr)
 pbox( x0+(i-1)*larg+i, y1-datr[i], larg, datr[i], clr )
end

function drawtab()
    pbox(x0+1,y0,119,120,0)
    for i=1,20 do
    drawbox(i,colour(datr[i]))
    end
end

function graduation(X0,Y0,ss)
local i
for i=0,11 do
pline(X0,Y0+i*10,X0-2*ss,Y0+i*10) 
pline(X0,Y0+i*10,X0,Y0+(i+1)*10)
end 
pline(X0,Y0+110,X0-2*ss,Y0+110)
end

-- Start
pclear()
pmenu({"A:About ", "S:Stats", "Q:Quit"})
pfont(1)
gendatr()
drawtab()
pmoveto(5,0) pcolor(95)
write("Sorting in Plua with ")
srtpp=ppopup(srttbl,0)
pcolor(255)
pmoveto(5,145)
reset = pbutton( "Reset" )
randm = pbutton( "Random" )
sortit = pbutton( "Sort It" )
graduation(x0,y0,1)
graduation(x1,y0,-1)
pline(x0,y0+50,x0-2,y0+50)
pline(x0,y1,x1,y1)
-- Main Loop
while 1 do
ev,id=pevent() 
if ev==ctlSelect then
 if id==randm then
    gendatr()
    drawtab()
 elseif id == reset then
    resetdatr()
    drawtab()
 elseif id == sortit then
    smod=pgetstate(srtpp) or 0
    cmps = 0
    swaps = 0
    functbl[smod+1]()
    drawtab()
  end
elseif ev==menuSelect then
       if id==1 then
          palert([[   Plua Sorting 1.1
written by: Hassoumi ZITOUN
modified by: Blake Winton <bwinton+plua@latte.ca>

Freely distributed. 
]])
    elseif id==2 then
          palert([[  Stats:
Comparisons: ]] .. cmps .. [[
Swaps: ]] .. swaps )
    elseif id==3 then
      exit()
    end
  end
end