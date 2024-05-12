# MSR90
> A journey into learning about magnetic strip data in modern day cards

#### WORK IN PROGRESS
**Hardware:** [Deftun MSR90 3 Track Reader](https://www.amazon.com/MSR90-Magnetic-Credit-Reader-Deftun/dp/B01DUB4GVO/)

## Legal Disclaimer
The information and code provided in this repository are intended for educational and research purposes only, focusing on magnetic stripe data security and the documentation of the MSR90 magnetic card reader. The author of this repository does not endorse or promote the use of this information for fraudulent or illegal activities. The content is provided "as is" without warranty of any kind, express or implied. Neither the author nor the contributors shall be held liable for any damages arising from the use of this information. Users are encouraged to comply with all applicable laws and regulations regarding magnetic stripe data usage.

## Information
This repository serves as a personal exploration of magnetic stripe data as used in modern payment systems. The focus is on understanding the formatting of magnetic strip data, the mechanics of how systems interpret this data, and the associated security risks and vulnerabilities.

Despite the widespread use of magnetic stripe technology in financial transactions, there is a notable scarcity of accessible information and practical code examples on this topic.

Let's hope we don't get Banned 🤷

###### Initial discover & observances
To my suprise, most of these card readers act as an HID that mimics a keyboard. Simply put, you swipe a card and it types the data out that is on the magnetic strip. Also to my suprise these work out of the box on Linux & Android systems.

## Financial Cards

There are up to three tracks on magnetic cards known as tracks 1, 2, and 3. Track 3 is virtually unused by the major worldwide networks, and often is not even physically present on the card by virtue of a narrower magnetic stripe. Point-of-sale card readers almost always read track 1, or track 2, and sometimes both, in case one track is unreadable. The minimum cardholder account information needed to complete a transaction is present on both tracks. Track 1 has a higher bit density *(210 bits per inch vs. 75)*, is the only track that may contain alphabetic text, and hence is the only track that contains the cardholder's name. 

### Track 1
Track 1 is written with code known as DEC SIXBIT plus odd parity.

![](./.screens/track1.png)

###### Format A
Reserved for proprietary use of the card issuer

###### Format B
| Item                                | Description                                          |
| ----------------------------------- | ---------------------------------------------------- |
| Start sentinel                      | 1 byte *(the % character)*                           |
| Format code                         | 1 byte alpha                                         |
| Primary account number (PAN)        | up to 19 characters *(may contain spaces sometimes)* |
| Field Separator                     | 1 byte *(the ^ character)*                           |
| Name                                | 2 to 26 characters, surnames separated by space if necessary, Surname separator: / |
| Field Separator                     | one character (generally '^') |
| Expiration date                     | four characters in the form YYMM. |
| Service code                        | three characters |
| Discretionary data                  | may include Pin Verification Key Indicator *(PVKI, 1 character)*, PIN Verification Value *(PVV, 4 characters)*, Card Verification Value or Card Verification Code *(CVV or CVC, 3 characters)* |
| End sentine                         | one character (generally '?')                                                        |
| Longitudinal redundancy check (LRC) | it is one character and a validity character calculated from other data on the track |

###### Format C-M
Reserved for use by ANSI Subcommittee X3B10

###### Format N-Z
Available for use by individual card issuers

### Track 2
This format was developed by the banking industry *(ABA)*. This track is written with a 5-bit scheme *(4 data bits + 1 parity)*, which allows for 16 possible characters, which are the numbers 0–9, plus the six characters  : ; < = > ? . *(ASCII range 0x30 through 0x3f)*

![](./.screens/track2.png)

| Item                                | Description |
| ----------------------------------- | ----------- |
| Start sentinel                      | 1 byte *(the ; character)*   |
| Primary account number (PAN)        | up to 19 characters *(may contain spaces sometimes)* |
| Separator                           | 1 byte *(the = character)*  |
| Expiration date                     | four characters in the form YYMM. |
| Service code                        | three digits. The first digit specifies the interchange rules, the second specifies authorization processing and the third specifies the range of services |
| Discretionary data                  | as in track one |
| End sentinel                        | one character (generally '?') |
| Longitudinal redundancy check (LRC) | it is one character and a validity character calculated from other data on the track. Most reader devices do not make the LRC available for display, but use it to verify the input internally to the device. |

#### Service Code
###### First digit
| Code | Description                                                                                |
| ---- | ------------------------------------------------------------------------------------------ |
| 1    | International interchange OK                                                               |
| 2    | International interchange, use IC *(chip)* where feasible                                  |
| 5    | National interchange only except under bilateral agreement                                 |
| 6    | National interchange only except under bilateral agreement, use IC *(chip)* where feasible |
| 7    | No interchange except under bilateral agreement *(closed loop)*                            |
| 9    | Test                                                                                       |

###### Second digit
| Code | Description                                                                              |
| ---- | ---------------------------------------------------------------------------------------- |
| 0    | Normal                                                                                   |
| 2    | Contact issuer via online means                                                          |
| 4    | Contact issuer via online means except under bilateral agreement                         |

###### Third digit
| Code | Description                                                 |
| ---- | ----------------------------------------------------------- |
| 0    | No restrictions, PIN required                               |
| 1    | No restrictions                                             |
| 2    | Goods and services only *(no cash)*                         |
| 3    | ATM only, PIN required                                      |
| 4    | Cash only                                                   |
| 5    | Goods and services only *(no cash)*, PIN required           |
| 6    | No restrictions, use PIN where feasible                     |
| 7    | Goods and services only *(no cash)*, use PIN where feasible |
___

###### Mirrors for this repository: [acid.vegas](https://git.acid.vegas/msr90) • [SuperNETs](https://git.supernets.org/acidvegas/msr90) • [GitHub](https://github.com/acidvegas/msr90) • [GitLab](https://gitlab.com/acidvegas/msr90) • [Codeberg](https://codeberg.org/acidvegas/msr90)
