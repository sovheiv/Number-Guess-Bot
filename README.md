## Guess the number
### Telegram bot
This is a telegram bot for the game Guess the number. 

This bot was running on ubuntu server on my Raspberry Pi.

Try it:
- Link: https://t.me/guess_a_number_bot
- Nickname: @guess_a_number_bot

This bot allows you not only guess but also think of numbers, and this bot will guess it within 7 tries

If you have any questions, write to me on Telegram https://t.me/sovheiv

### How to run it on Raspberry:
1. Install ubuntu server LTS 64-bit version on sd-card
2. Update network-config file
3. Run Raspberry
4. Connect by ssh 
5. [install mongodb v4.4](https://www.mongodb.com/developer/how-to/mongodb-on-raspberry-pi/)
6. Instal pip: sudo apt install python3-pip
7. Instal virtualenv: python3.8 -m pip install virtualenv
8. Create venv: python3.8 -m virtualenv venv
9. Enter venv and install requirements
10. Check it. Run your bot 
11. Create .sh file 
12. Create unit in /etc/systemd/system/
14. Set autostart your unit: sudo systemctl enable application



