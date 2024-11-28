def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


prof = 11.1
ac = 21

crit_fail = 0
fail = 0
hit = 0
crit_hit = 0

# 1
# clutch?
if prof + 1 >= ac + 10:
    hit += 5
elif prof + 1 >= ac:
    fail = +5
else:
    crit_fail += 5
# 2-19
for x in range(18):
    if prof + 2 + x >= ac + 10:
        crit_hit += 5
    elif prof + 2 + x >= ac:
        hit += 5
    elif prof + 2 + x <= ac - 10:
        crit_fail += 5
    else:
        fail += 5
# 20
if prof + 20 >= ac:
    crit_hit += 5
elif prof + 20 >= ac - 10:
    hit += 5
else:
    fail += 5

print(f"crit hit:{crit_hit}%")
print(f"hit:{hit}%")
print(f"fail:{fail}%")
print(f"crit fail:{crit_fail}%")
print()

# a minToHit value of 11.2 means that when the dice rolls 11
# there's a 20% chance of it being a failure
# and 80% chance of it being a hit
# so it would be a total of 59% chance to hit before subtracting critical hits

# 2-19
diceFacesUsed = 0

# defender's critical ac minus attacker's modifier and a +1 to create an offset and start at a dice value 2
minToCrit = (ac + 10) - prof + 1
sidesThatCritHit = clamp(21 - minToCrit, 0, 18 - diceFacesUsed)
diceFacesUsed += sidesThatCritHit

minToHit = (ac) - prof + 1
sidesThatHit = clamp(21 - minToHit - diceFacesUsed, 0, 18 - diceFacesUsed)
diceFacesUsed += sidesThatHit

minToFail = (ac - 9) - prof + 1
sidesThatFail = clamp(21 - minToFail - diceFacesUsed, 0, 18 - diceFacesUsed)
diceFacesUsed += sidesThatFail

sidesThatCritFail = 18 - diceFacesUsed

print(round(sidesThatCritHit, 3))
print(round(sidesThatHit, 3))
print(round(sidesThatFail, 3))
print(round(sidesThatCritFail, 3))

# 1
Nat1Value = prof + 1
if Nat1Value >= ac + 10:
    value = clamp(Nat1Value - ac + 10 + 1, 0, 1)
    sidesThatHit += value
    sidesThatFail += 1 - value
elif Nat1Value >= ac:
    value = clamp(Nat1Value - ac + 1, 0, 1)
    sidesThatFail += value
    sidesThatCritFail += 1 - value
else:
    sidesThatCritFail += 1
# 20
Nat20Value = prof + 20
if Nat20Value >= ac:
    value = clamp(Nat20Value - ac + 1, 0, 1)
    sidesThatCritHit += value
    sidesThatHit += 1 - value
elif Nat20Value >= ac - 10:
    value = clamp(Nat20Value - ac + 10 + 1, 0, 1)
    sidesThatHit += value
    sidesThatFail += 1 - value
else:
    sidesThatFail += 1

sidesThatCritHit = round(sidesThatCritHit, 3)
sidesThatHit = round(sidesThatHit, 3)
sidesThatFail = round(sidesThatFail, 3)
sidesThatCritFail = round(sidesThatCritFail, 3)

print()
print(sidesThatCritHit)
print(sidesThatHit)
print(sidesThatFail)
print(sidesThatCritFail)
