-- Sort Simple Funcs.lua

function sel()
local k,j,mx
  for k=1,n-1 do
    mx=k
    for j=k+1,n do
      if lt(j,mx) then mx=j end
    end
    swap(k,mx)
  end
end

function ins()
local i,j
  for i=1,n-1 do
    j=i
    while j>0 do
      if lt(j+1,j) then
        swap(j,j+1)
      else
        break
      end
     j=j-1
    end
 end
end

function bub()
local i,j,b
  for i=n-1,1,-1 do
    b=0
    for j=1,i do  
      if lt(j+1,j) then
        swap(j+1,j)
        b=1
      end
    end
    if b==0 then
      break
    end
  end
end

function bibub()
local i,j,b
  for i=1,floor(n/2)+1 do
    b=0
    for j=i,n-i  do  
      if lt(j+1, j) then
        swap(j+1, j)
        b=1
      end
    end
    if b==0 then break end
    for j=n-i,i,-1do  
      if lt(j+1, j) then
        swap(j+1, j)
        b=1
      end
    end
    if b==0 then break end
  end
end

tinsert( srttbl, "Select" )
tinsert( functbl, sel )
tinsert( srttbl, "Insert" )
tinsert( functbl, ins )
tinsert( srttbl, "Bubble" )
tinsert( functbl, bub )
tinsert( srttbl, "Bi-Di Bubble" )
tinsert( functbl, bibub )