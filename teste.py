cat = ['Aluguel','Agua','Lazer']
print(cat)

nova_cat = 'A'
cat = cat + [nova_cat] if nova_cat not in cat else cat

print(cat)

nova_cat = 'Aluguel'
cat = cat + [nova_cat] if nova_cat not in cat else cat

print(cat, 'novo')