"""
✘ Commands Available -

• `{i}get var <variable name>`
   Get value of the given variable name.

• `{i}get type <variable name>`
   Get variable type.

• `{i}get redis <key>`
   Get redis value of the given key.

• `{i}get keys`
   Get all redis keys.
"""

import os

from . import *


@ultroid_cmd(pattern="get")
async def get_var(event):
    x = await eor(event, get_string("com_1"))
    if not event.out and not is_fullsudo(event.sender_id):
        return await eod(event, "`This Command Is Sudo Restricted.`")
    try:
        opt = event.text.split(" ", maxsplit=2)[1]
    except IndexError:
        return
    if not opt == "keys":
        try:
            varname = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            return await eod(x, "Such a var doesn't exist!", time=5)
    if opt == "var":
        c = 0
        # try redis
        val = udB.get(varname)
        if val is not None:
            c += 1
            return await x.edit(
                f"**Variable** - `{varname}`\n**Value**: `{val}`\n**Type**: Redis Key."
            )
        # try env vars
        val = os.getenv(varname)
        if val is not None:
            c += 1
            return await x.edit(
                f"**Variable** - `{varname}`\n**Value**: `{val}`\n**Type**: Env Var."
            )

        if c == 0:
            return await eod(x, "Such a var doesn't exist!", time=5)

    elif opt == "type":
        c = 0
        # try redis
        val = udB.get(varname)
        if val is not None:
            c += 1
            return await x.edit(f"**Variable** - `{varname}`\n**Type**: Redis Key.")
        # try env vars
        val = os.getenv(varname)
        if val is not None:
            c += 1
            return await x.edit(f"**Variable** - `{varname}`\n**Type**: Env Var.")

        if c == 0:
            return await eod(x, "Such a var doesn't exist!", time=5)

    elif opt == "redis":
        val = udB.get(varname)
        if val is not None:
            return await x.edit(f"**Key** - `{varname}`\n**Value**: `{val}`")
        else:
            return await eod(x, "No such key!", time=5)

    elif opt == "keys":
        keys = sorted(udB.keys())
        msg = ""
        for i in keys:
            if i.isdigit() or i.startswith("-") or i.startswith("GBAN_REASON_"):
                pass
            else:
                msg += f"• `{i}`" + "\n"
        await x.edit(f"**List of Redis Keys :**\n{msg}")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
