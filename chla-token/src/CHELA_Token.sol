// SPDX-License-Identifier: MIT
pragma solidity ^0.8.33;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract CHELA_Token is ERC20 {
    constructor() ERC20("CHELA Token", "CHLA") {
        // ผลิตเหรียญ 10,000,000,000 CHLA ตามสเปกที่ท่านประธานกำหนด
        _mint(msg.sender, 10000000000 * 10**decimals());
    }
}
