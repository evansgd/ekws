# :key: Embed Key With Steganography

This is a quick and dirty POC implementation of an algorithm described in this [paper](https://www.researchgate.net/publication/265209062_Encryption_Key_Distribution_Applying_Steganographic_Techniques). The algorithm prescribes a way to embed a cryptographic key into a cipher text. I thought it would be fun and interesting to do. By no means does this implementation is secure. Moreover, the program offers no way to parametrize the protocol. Finally, note that I split by group of 1 byte the key which, from my understanding, is allowed by the protocol but is not a strict rule. I did so for it was easier for me to reason about the algorithm and it simplifies the code a wee bit.

## :oncoming_automobile: Getting Started

Follow the instructions below to experiment with the program.

### :mortar_board: Prerequisites

You need to have docker installed on your system. 

### :rocket: Run

Simply run this command to fire up a bash shell:
```
docker run --rm -it -v $PWD:/code --workdir /code python:3.9-slim-buster bin/bash
#OR
./start.sh
```
Then install the needed libraries,

```
pip install -r requirements.txt
```
Run the program
```
python run.py --message "I love Crytopgrahy and Steganography" --loci '12,28,8,13,24,7,34,29,47,1,25,0,3,15,10,14,38,20,35,37,43,23,42,11,36,32,2,33,17,21,45,22,27,44,41,18,9,46,31,40,4,19,26,16,5,6,39,30'
```
where 

```message``` is the plain text (utf-8) you want to encrypt (**_AES_**);

```loci``` are the positions where the sub-keys will be placed. Ideally, as a rule of thumb, use 48 different index positions (since the cryptographic key generated is 48 bytes-long);
### :hammer: Tests

This command will run the unit test(s) (assuming that you are at the root of the project):
```
python -m unittest discover tests
```

## :page_with_curl: License

This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
