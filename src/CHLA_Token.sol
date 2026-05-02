// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract ChelayaToken is ERC20 {
    constructor() ERC20("CHELA Asset", "CHLA") {
        /**
         * @dev การมินต์เหรียญทั้งหมด 10,000,000,000 (10 พันล้าน) 
         * เหรียญจะถูกส่งเข้าไปที่กระเป๋าที่ใช้ Deploy ทันที
         */
        _mint(msg.sender, 10000000000 * 10 ** decimals());
    }
}
