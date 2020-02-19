var current = new Date();
var currentMonth = current.getMonth();
var currentDate = current.getDate();
var currentYear = current.getFullYear();

function calender(month, year) {
    var padding = "";

    febDays = ((currentYear % 100 !== 0) && (currentYear % 4 === 0) || (currentYear % 400 === 0)) ? 29 : 28;

    var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var numberOfDays = ["31", String(febDays), "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"];

    var firstDate = new Date(monthNames[month] + ' 1, ' + year);
    var firstDay = firstDate.getDay();
    var totalDays = numberOfDays[month];

    for (var i = 0; i < firstDay; i++) {
        padding += "<td class='preMonth'></td>";
    }

    var generateDay = firstDay;
    var generateCal = "";

    for (var i = 1; i <= totalDays; i++) {
        if (generateDay > 6) {
            generateCal += "</tr><tr>";
            generateDay = 0;
        }

        if (i == currentDate && month == currentMonth) {
            generateCal += "<td onclick='td_click(event);' class='currentday' id='" + i + monthNames[month] + "'><span class='date'>" + i + "</span><div class='insert_cal'></div></td>";
        } else {
            generateCal += "<td onclick='td_click(event);'  id='" + i + monthNames[month] + "'><span class='date'>" + i + "</span><div class='insert_cal'></div></td>";
        }

        generateDay++;
    }

    var calenderTable = "<table>";

    if ($(window).width() < 750) {
        calenderTable += "<tr class='table-header'> <th>일</th> <th>월</th> <th>화</th> <th>수</th> <th>목</th> <th>금</th> <th>토</th> </tr>";
    } else {
        calenderTable += "<tr class='table-header'> <th>일요일</th> <th>월요일</th> <th>화요일</th> <th>수요일</th> <th>목요일</th> <th>금요일</th> <th>토요일</th> </tr>";
    }
    calenderTable += "<tr>";
    calenderTable += padding;
    calenderTable += generateCal;
    calenderTable += "</tr></table>";

    $(".container").html(calenderTable);
    $(".month").text(monthNames[month]);
    $(".month").attr('id', month);
    $(".year").text(year);
    $(".year").attr('id', year);
}

function nextMonth() {
    if ($(".month").attr('id') != 11) {
        var nextMon = Number($(".month").attr('id')) + 1;
        var year = Number($(".year").attr('id'));
    } else {
        var nextMon = 0;
        var year = Number($(".year").attr('id')) + 1;
    }
    calender(nextMon, year);
    refreshAllEvents();
    monthKorean();
}

function prevMonth() {
    if ($(".month").attr('id') != 0) {
        var prevMon = Number($(".month").attr('id')) - 1;
        var year = Number($(".year").attr('id'));
    } else {
        var prevMon = 11;
        var year = Number($(".year").attr('id')) - 1;
    }
    calender(prevMon, year);
    refreshAllEvents();
    monthKorean();
}


if (window.addEventListener) {
    calender(currentMonth, currentYear);
    refreshAllEvents();
} else if (window.attachEvent) {
    calender(currentMonth, currentYear);
    refreshAllEvents();
}


$(window).resize(function() {
    if ($(window).width() < 750) {
        $(".table-header").html("<th>일</th> <th>월</th> <th>화</th> <th>수</th> <th>목</th> <th>금</th> <th>토</th>");
    } else {
        $(".table-header").html("<th>일요일</th> <th>월요일</th> <th>화요일</th> <th>수요일</th> <th>목요일</th> <th>금요일</th> <th>토요일</th");
    }
});


$(document).ready(function(){
    monthKorean();
});

function monthKorean() {
    var string = document.getElementsByClassName("month")[0].innerHTML;
    
    if (string == "January") {
        var replacedString = string.replace("January", "1");}
    else if (string == "February") {
        var replacedString = string.replace("February", "2");}
    else if (string == "March") {
        var replacedString = string.replace("March", "3");}
    else if (string == "April") {
        var replacedString = string.replace("April", "4");}
    else if (string == "May") {
        var replacedString = string.replace("May", "5");}
    else if (string == "June") {
        var replacedString = string.replace("June", "6");}
    else if (string == "July") {
        var replacedString = string.replace("July", "7");}
    else if (string == "August") {
        var replacedString = string.replace("August", "8");}
    else if (string == "September") {
        var replacedString = string.replace("September", "9");}
    else if (string == "October") {
        var replacedString = string.replace("October", "10");}
    else if (string == "November") {
        var replacedString = string.replace("November", "11");}
    else if (string == "December") {
        var replacedString = string.replace("December", "12");}
    
    document.getElementsByClassName("month")[0].innerHTML = replacedString;
} 