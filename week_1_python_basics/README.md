# MTN MoMo Balance Check (Simulation)

A command-line Python script that simulates the MTN MoMo USSD flow for
checking an account balance.

Zaptek Internship — Backend Engineering with FastAPI (Team 2)
Week 1: Python Basics

## What it does

Reproduces the `*170#` menu flow used to check a MoMo wallet balance:

Main menu -> 6) My Wallet -> 1) Check Balance -> enter PIN -> balance


The PIN is `2345`, as specified in the task brief. Entering it correctly
displays the wallet balance. Three consecutive wrong PINs block the wallet.

## Requirements

Python 3.6 or later. No third-party packages.

## Running it

```bash
python momo.py
```

## Where the menu structure came from

The menus were transcribed from a live `*170#` session on an MTN Ghana
line on 17 September 2026, rather than from documentation — published
guides disagreed with each other on the menu numbering.

Two items were merged back together during transcription. The USSD gateway
splits long messages across screens at a character limit, which had cut
`Financial Services` and `Change & Reset PIN` in half mid-item. Those
splits are a transport artifact, not menu structure.

## Design notes

Logic is kept separate from input and output. `verify_pin`,
`is_valid_pin_format` and `format_balance` take arguments and return
values without printing, so they can be tested directly. All user
interaction happens in the flow functions.

Menus are stored as lists and rendered by a single `display_menu`
function, so both menus share one implementation rather than each having
its own block of print statements.

The balance is stored in **pesewas** (the smallest currency unit) as an
integer, and converted only for display. Storing money as a float invites
rounding errors — `0.1 + 0.2` is not `0.3` in binary floating point.

Menu options are 1-based on screen and 0-based in the list. The
conversion happens in exactly one place, inside `get_menu_choice`, which
returns a list index. Everything downstream works in indices.

## Simulation limits

This is a simulation, not an integration with MTN. Specifically:

- The balance is a hardcoded constant. Real MoMo reads it from MTN's
  ledger over the network.
- Real MoMo also delivers the balance by SMS. This script only prints
  to the terminal.
- The wrong-PIN counter resets each run. MTN's counter persists across
  sessions.
- The wording of the PIN prompt and the balance message is approximated.
  The menu text itself is verbatim.
- Menu pagination (`# for next`, `0) Back`) is not implemented; all
  options are listed on one screen.
- Only the Check Balance path is implemented. Every other menu option
  reports that it is unavailable in the simulation.

## Author

Joseph Boafo Afful