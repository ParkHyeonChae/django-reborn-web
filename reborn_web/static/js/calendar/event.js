var month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var month_number = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];
var day_name = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var year = parseInt($(".year").attr('id'));

function td_click(event) {
	event.stopPropagation();
	closeEveBox(event);

	var td_id = event.target.id;
	if (td_id == "") {
		td_id = event.target.closest("td").id;
	}

	$("#eventName").val("");
	$("#eventLocation").val("");
	$("#eventDescription").val("");
	$("#eventStartDate, #eventEndDate").attr("disabled", true);
	$("#eventAllDay").removeClass("fa-square").addClass("fa-check-square");

	var td_date = parseInt(td_id);
	var td_month = td_id.substr(td_date.toString().length);
	
	setStartEndDate(td_date, td_month);
	// $(".eveBoxDate").text(td_date + " " + td_month + " " + year);
	$(".eveBoxDate").text("일정 추가");
	// $(".eveBoxDate").text(year+"년"+" "+td_month+"월"+" "+td_date+"일");

	$("#" + td_id).append("<div id='justForShowEvent'></div>");
	var td_left = $("#" + td_id).position().left;
	var td_width = $("#" + td_id).width();
	var windowWidth = $(window).width();
	var eventBoxWidth = $("#addEvent").width();
	if (td_left + td_width + eventBoxWidth > windowWidth) {
		$("#addEvent").show().css({position:"absolute", top:(event.pageY - 120), left: (td_left - eventBoxWidth)});
	} else {
		$("#addEvent").show().css({position:"absolute", top:(event.pageY - 120), left: (td_left + td_width + 8)});
	}
}

function setStartEndDate(date, month) {
	if (date < 10) {date = "0" + date};
	month = month_number[month_names.indexOf(month)];

	$("#eventStartDate").val(year + "-" + month + "-" + date);
	$("#eventEndDate").val(year + "-" + month + "-" + date);
}
 
function closeEveBox(e) {
    e.preventDefault();
    
	$("#justForShowEvent").remove();
	$(".event-rectangles").removeClass("event-rectangle-select");
	$("#addEvent").hide();
    $("#viewEvent").hide();
}

function resetCloseEveBox(e) {
    e.preventDefault();
    
	$("#justForShowEvent").remove();
	$(".event-rectangles").removeClass("event-rectangle-select");
	$("#addEvent").hide();
    $("#viewEvent").hide();
    $("#eventId").val("");
}

function allDay() {
	if ($(".fa-check-square").length) {
		$("#eventStartDate, #eventEndDate").attr("disabled", false);
		$("#eventAllDay").removeClass("fa-check-square").addClass("fa-square");
	} else {
		$("#eventStartDate, #eventEndDate").attr("disabled", true);
		$("#eventAllDay").removeClass("fa-square").addClass("fa-check-square");
	}
}

function updateEvent(e) {
	e.preventDefault();

	$("#error").text("");
	var eventId = $("#eventId").val();
	var eventName = $("#eventName").val();
	var eventLocation = $("#eventLocation").val();
	var eventStartDate = String($("#eventStartDate").val());
	var eventEndDate = String($("#eventEndDate").val());
	var eventDescription = $("#eventDescription").val();
	if ($(".fa-check-square").length) {
		var eventAllDay = 1;
	}
	else
		var eventAllDay = 0;

	if (eventStartDate > eventEndDate) {
		$("#error").text("날짜를 정확히 입력해주세요.");
	} else if (eventStartDate.substr(0, 7) != eventEndDate.substr(0, 7)) {
		$("#error").text("한달 내의 일정만 등록이 가능합니다.");
	} else {
		$.getJSON("updateEvent/", {eventId: eventId, eventName: eventName, eventLocation: eventLocation, eventStartDate: eventStartDate, eventEndDate: eventEndDate, eventAllDay: eventAllDay, eventDescription: eventDescription}, function(data) {
			$("#status").text(data["result"]);
			$("#justForShowEvent").remove();
            $("#addEvent").hide();
            $("#eventId").val("");
			refreshAllEvents();
		});
	}
}

function event_rectangle_clicked(event) {
	event.stopPropagation();
	closeEveBox(event);

	// $(".viewEveBoxName").text(event.target.innerHTML);
	var event_id = event.target.id;
	$("[id=" + event_id + "]").addClass("event-rectangle-select");
	$("#viewEveBoxEveId").text(event_id);
	$.getJSON("viewEvent/", {eventId: event_id}, function(data) {
		$(".viewEveBoxName").text(data["event_name"]);
		$(".viewTitle").text(data["event_name"]);
		$(".viewLocation").text(data["location"]);
		$(".viewDescription").text(data["description"]);
		
		// if (data["description"] != "") {
		// 	$(".viewDescription").text(data["description"]);
		// }
		
		var start_date = new Date(data["start_date"].replace(/-/g,'/'));
		var day_num = start_date.getDay();
		var day = day_name[day_num];
		var date = parseInt(data["start_date"].substr(8,2));
		var month = month_names[parseInt(data["start_date"].substr(5,2)) - 1];

		if (data["all_day"] == true) {
			$(".viewDay").text(day + ", " + month + " " + date);
		}

		var parent_td = $("#" + event.target.id).parent();
		var parent_td_left = parent_td.position().left;
		var parent_td_width = parent_td.width();
		var windowWidth = $(window).width();
		var eventBoxWidth = $("#viewEvent").width();
		if (parent_td_left + parent_td_width + eventBoxWidth + 30 > windowWidth) {
			$("#viewEvent").show().css({position:"absolute", top:(event.pageY - 120), left: (parent_td_left - eventBoxWidth)});
		} else {
			$("#viewEvent").show().css({position:"absolute", top:(event.pageY - 120), left: (parent_td_left + parent_td_width + 8)});
		}
	});
}

function deleteEve(event) {
	event.preventDefault();
	event.stopPropagation();

	var event_id = $("#viewEveBoxEveId").text();

	$.getJSON("forceDelete/", {eventId: event_id}, function(data) {
		$("#status").text(data["result"]);
		closeEveBox(event);
		refreshAllEvents();
	});
}

function editEve(event) {
	event.preventDefault();
	event.stopPropagation();

	var event_id = $("#viewEveBoxEveId").text();

	$.getJSON("viewEvent/", {eventId: event_id}, function(data) {
		$("#eventId").val(event_id);
		$("#eventName").val(data["event_name"]);
		$("#eventLocation").val(data["location"]);
		$("#eventStartDate").val(data["start_date"]);
		$("#eventEndDate").val(data["end_date"]);
		$("#eventDescription").val(data["description"]);
		if (data["all_day"] == true) {
			$("#eventStartDate, #eventEndDate").attr("disabled", true);
			$("#eventAllDay").removeClass("fa-square").addClass("fa-check-square");
		} else {
			$("#eventStartDate, #eventEndDate").attr("disabled", false);
			$("#eventAllDay").removeClass("fa-check-square").addClass("fa-square");
		}
		var date = parseInt(data["start_date"].substr(8,2));
		var month = month_names[parseInt(data["start_date"].substr(5,2)) - 1];

		// if (td_month == "January") {
		// 	td_month = "1"}
		// else if (td_month == "February") {
		// 	td_month = "2"}
		// else if (td_month == "March") {
		// 	td_month = "3"}
		// else if (td_month == "April") {
		// 	td_month = "4"}
		// else if (td_month == "May") {
		// 	td_month = "5"}
		// else if (td_month == "June") {
		// 	td_month = "6"}
		// else if (td_month == "July") {
		// 	td_month = "7"}
		// else if (td_month == "August") {
		// 	td_month = "8"}
		// else if (td_month == "September") {
		// 	td_month = "9"}
		// else if (td_month == "October") {
		// 	td_month = "10"}
		// else if (td_month == "November") {
		// 	td_month = "11"}
		// else if (td_month == "December") {
		// 	td_month = "12"}
		
		$(".eveBoxDate").text("일정 수정");
		// $(".eveBoxDate").text(date + " " + month + " " + year);
		// $(".eveBoxDate").text(year+"년"+" "+td_month+"월"+" "+date+"일");

		closeEveBox(event);
		$("#" + event_id).addClass("event-rectangle-select");
		if ($(window).width() > 750) {
			$("#addEvent").show().css({position: "absolute", top: (event.pageY - 375), left: (event.pageX - 220)});
		} else {
			$("#addEvent").show().css({position: "absolute", top: (event.pageY - 235), left: (event.pageX - 110)});
		}
	});
}

function refreshAllEvents() {

	$(".event-rectangles").remove();

	$.get("allEvents/", function(data) {
		var event_id_end_date = data.split(";");
		var event_list = [];
		for (var i = 0; i < event_id_end_date.length - 1; i++) {
			event_list.push({
				event_id: event_id_end_date[i].split("/")[0],
				end_date: event_id_end_date[i].split("/")[1],
				event_name: event_id_end_date[i].split("/")[2],
			});
		}

		for (var i = 0; i < event_list.length; i++) {
			var eventStartDate = event_list[i]["event_id"].substr(6, 10);
			var eventEndDate = event_list[i]["end_date"];
			var eventId = event_list[i]["event_id"];
			var eventName = event_list[i]["event_name"];

			if (eventStartDate == eventEndDate) {
				eventDivId = parseInt(eventStartDate.substr(8, 2)) + month_names[month_number.indexOf(eventStartDate.substr(5, 2))];
				$("#" + eventDivId).append("<div onclick='event_rectangle_clicked(event);' class='event-rectangles' id='" + eventId +"'>" + eventName + "</div>");
			} else {
				var Date1 = eventStartDate;
				var Date2 = eventEndDate;
				Date1 = new Date(Date1.replace(/-/g,'/'));
				Date2 = new Date(Date2.replace(/-/g,'/'));
				var timeDiff = Math.abs(Date2.getTime() - Date1.getTime());
				var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); 

				var R = Math.floor(Math.random()*180)+50; 
				// var G = get_random_integer ( 0, 255 ); 
				// var B = get_random_integer ( 0, 255 ); 

				var random_color = "rgb(" + R+ ",0"+ ",0)"
				for (var j=0; j <= diffDays; j++) {
					eventDivId = parseInt(eventStartDate.substr(8, 2)) + j + month_names[month_number.indexOf(eventStartDate.substr(5, 2))];
					if(j!=0) eventName="";

					$("#" + eventDivId).children('.insert_cal').prepend("<div onclick='event_rectangle_clicked(event);' style='background-color:"+ random_color +";' class='event-rectangles joint-event' id='" + eventId +"'>" + eventName + "</div>");
				}
			}
		}
	});
}