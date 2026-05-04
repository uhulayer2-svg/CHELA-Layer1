// SPDX-License-Identifier: MIT
pragma solidity ^0.8.33;

import "forge-std/Script.sol";
import {CHELA_Token} from "../src/CHELA_Token.sol"; 

contract DeployAndDistribute is Script {
    function run() external {
        // ตัดการดึงจาก env ออก เพื่อใช้ค่าจาก --private-key ใน command line โดยตรง
        vm.startBroadcast();

        CHELA_Token token = new CHELA_Token(); 

        vm.stopBroadcast();
    }
}
