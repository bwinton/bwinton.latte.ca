-- Sort Complex Funcs.lua

function hBubDn(i, n)
local j
  j = 2 * i
  if j < n and lt(j, j+1) then
    j = j + 1
  end
  while j <= n and lt(i, j) do
    swap(i, j)
    i = j
    j = 2 * i
    if j < n and lt(j, j+1) then
      j = j + 1
    end
  end
end

function hDelMax(i)
    swap(1, i)
    i = i - 1
    hBubDn(1, i)
end

function heap()
local i,j,tmp
  for i=floor(n/2),1, -1 do
    hBubDn(i, n)
  end
  for i=n,1, -1 do
    hDelMax(i)
  end
end

function mMerge(i, j)
local s
  s = floor( (j-i+1)/2 ) + i
  while i<=s and s<=j do
    if lt(s, i) then
      swap(s, i)
      for y=s,i+2,-1 do
        swap(y-1, y)
      end
      s=s+1
   end
   i=i+1
  end
end

function mBody( i, j )
local s
  if j == i then
    return
  end
  s = floor( (j-i+1)/2 ) + i
  mBody(i, s-1)
  mBody(s, j)
  mMerge(i, j)
end

function merge()
   mBody(1, n )
end

function shell()
local h,i,j
  h=1
  while h<=n do
    h=h*3+1
  end
  while h>1 do
    h=(h-1)/3
    for j=1,n-h do
      for i=j,1,-h do
        if lt(i,i+h) then
          break
        end
        swap(i,i+h)
      end
    end
  end
end

function qBody(i,j)
local p,u,d
  if i>=j then return end
  p=i
  u=i+1
  d=j
  while u<d do
    while u<d and lte(u,p) do
      u=u+1
    end
    while u<d and lt(p,d)do
      d=d-1
    end
    if u<d then
      swap(u,d)
    end
  end
  if lt(p,d) then
    d=d-1
  end
  swap(d,p)
  qBody(i,d-1)
  qBody(d+1,j)
end

function quick()
   qBody(1, n )
end

function comb()
local j,d
  d = n
  while d>1 do
    d = floor( 10*d/13 )
    if d > 8 and d < 11 then
      d = 11
    end
    for j=1,n-d do
      if lt(j+d,j) then
        swap(j+d,j)
      end
    end
  end
end

tinsert( srttbl, "Heap" )
tinsert( functbl, heap )
tinsert( srttbl, "Merge" )
tinsert( functbl, merge )
tinsert( srttbl, "Shell" )
tinsert( functbl, shell )
tinsert( srttbl, "Quick" )
tinsert( functbl, quick )
tinsert( srttbl, "Comb" )
tinsert( functbl, comb )