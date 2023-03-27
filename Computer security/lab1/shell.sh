#!/bin/bash
echo "$ python3 password_manager.py init masterPassword"
python3 password_manager.py init masterpass
echo "$ python3 password_manager.py put masterPassword www.luka.hr sifra123ABC"
python3 password_manager.py put masterPassword www.luka.hr sifra123ABC
echo "$ python3 password_manager.py get masterPassword www.fer.hr"
python3 password_manager.py get masterPassword www.fer.hr 
echo "$ python3 password_manager.py put masterPassword www.ferko.hr Ferko123FER"
python3 password_manager.py put masterPassword www.ferko.hr Ferko123FER
echo "$ python3 password_manager.py put masterPassword www.ferko.hr FER123FERKOoo"
python3 password_manager.py put masterPassword www.ferko.hr FER123FERKOoo
echo "$ python3 password_manager.py get masterPassword www.ferko.hr"
python3 password_manager.py get masterPassword www.ferko.hr
echo "$ python3 password_manager.py get masterrPasword www.fer.hr"
python3 password_manager.py get masterrPasword www.fer.hr
read -p "Press Enter to continue."
