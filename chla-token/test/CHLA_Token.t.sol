// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/CHLA_Token.sol";

contract CHLATokenTest is Test {
    // แก้จาก CHLA_Token เป็น ChelayaToken ให้ตรงกับใน src
    ChelayaToken public chla; 
    address public mainTreasury = 0x2Eeb0f207C8CF5Fe5F74F50D54572183FDF1087c;

    function setUp() public {
        // ต้องใช้ชื่อ ChelayaToken ในการ New Contract ด้วยครับ
        chla = new ChelayaToken(); 
    }

    function test_InitialSupply() public {
        // ตรวจสอบยอด 10,000,000,000 CHLA
        uint256 expectedSupply = 10_000_000_000 * 10**18;
        assertEq(chla.totalSupply(), expectedSupply);
    }
}
