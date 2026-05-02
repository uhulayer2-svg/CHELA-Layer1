// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/CHLA_Token.sol";

contract DeployAndDistribute is Script {
    function run() external {
        // เริ่มต้นการใช้งาน Private Key จากเครื่อง X99
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        
        vm.startBroadcast(deployerPrivateKey);

        // 1. Deploy เหรียญ ChelayaToken หมื่นล้านเหรียญ
        ChelayaToken chla = new ChelayaToken();

        // 2. แสดงสถานะความสำเร็จ
        console.log("ChelayaToken deployed at:", address(chla));
        console.log("Total Supply: 10,000,000,000 CHLA");

        vm.stopBroadcast();
    }
}
