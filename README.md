# MSR90
> A journey into learning about magnetic strip data in modern day cards

#### WORK IN PROGRESS
**Hardware:** [Deftun MSR90 3 Track Reader](https://www.amazon.com/MSR90-Magnetic-Credit-Reader-Deftun/dp/B01DUB4GVO/)

## Information
To startoff, this is not for committing fraud. I will be documenting all my research on magnetic strip data aswell at writing code for it. For some reason it seems hard to find code  or any valid documentation on working with magnetic strip data on Linux, so this will attempt to be a deep dive into understanding the capabilities. This is simply academic research & for testing on your own data.

## Financial Cards

#### Track 1
###### Format B
| Item                                | Description |
| ----------------------------------- | ----------- |
| Start sentinel                      | one character (generally '%') |
| Format code="B"                     | one character (alpha only)    |
| Primary account number (PAN)        | up to 19 characters. Usually, but not always, matches the credit card number printed on the front of the card. |
| Field Separator                     | one character (generally '^') |
| Name                                | 2 to 26 characters, surnames separated by space if necessary, Surname separator: / |
| Field Separator                     | one character (generally '^') |
| Expiration date                     | four characters in the form YYMM. |
| Service code                        | three characters |
| Discretionary data                  | may include Pin Verification Key Indicator (PVKI, 1 character), PIN Verification Value (PVV, 4 characters), Card Verification Value or Card Verification Code (CVV or CVC, 3 characters) |
| End sentine                         | one character (generally '?')                                                        |
| Longitudinal redundancy check (LRC) | it is one character and a validity character calculated from other data on the track |

#### Track 2
This format was developed by the banking industry (ABA). This track is written with a 5-bit scheme (4 data bits + 1 parity), which allows for sixteen possible characters, which are the numbers 0–9, plus the six characters  : ; < = > ? . (It may seem odd that these particular punctuation symbols were selected, but by using them the set of sixteen characters matches the ASCII range 0x30 through 0x3f.) The data format is as follows:

| Item                                | Description |
| ----------------------------------- | ----------- |
| Start sentinel                      | one character (generally ';') |
| Primary account number (PAN)        | up to 19 characters. Usually, but not always, matches the credit card number printed on the front of the card. |
| Separator                           | one character (generally '=') |
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
| 5    | Goods and services only (no cash), PIN required             |
| 6    | No restrictions, use PIN where feasible                     |
| 7    | Goods and services only *(no cash)*, use PIN where feasible |
___

###### Mirrors for this repository: [acid.vegas](https://git.acid.vegas/msr90) • [SuperNETs](https://git.supernets.org/acidvegas/msr90) • [GitHub](https://github.com/acidvegas/msr90) • [GitLab](https://gitlab.com/acidvegas/msr90) • [Codeberg](https://codeberg.org/acidvegas/msr90)