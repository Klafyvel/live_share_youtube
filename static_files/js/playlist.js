 // 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');
var current_link = -1;
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var last_sync = new Date().getTime();
// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '390',
          width: '640',
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
          }
        });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
  if(tracks.length > 0 && current_link < (tracks.length - 1)) {
      next();
  }
  setInterval(loadLinks, 5000);
}

function play() {
      player.loadVideoById(tracks[current_link]);
      player.playVideo();
      document.getElementById(current_link).classList.add('bg-success');
      document.getElementById(current_link).classList.remove('bg-secondary');
}
function next() {
	if (current_link < (tracks.length -1)) {
      current_link += 1;
      play();
	}
}

function prev() {
	if (current_link > 0) {
      current_link -= 1;
      play();
	}
}

function setCurrent(c) {
    if(c > 0 && c < tracks.length) {
		document.getElementById(current_link).classList.remove('bg-success');
		document.getElementById(current_link).classList.add('bg-secondary');
        current_link = c;
        play();
    }
}

function setCurrentFromToken(token) {
    setCurrent(tracks.lastIndexOf(token));
}

function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.ENDED) {
	next();
  }
}
function stopVideo() {
  player.stopVideo();
}
function addLink() {
    var form = $('#add_link_form');
	$.ajax({
		type: "post",
		url: add_url,
		data: form.serialize(),
		async: true,
		success: loadLinks,
	})
	$('#id_url').val('');
	return false;
}
function updateLinks(data) {
	if (!data.updated) {
		return;
	}
	last_sync = new Date().getTime();
	var links = document.getElementById("links");
	while (links.firstChild) {
		    links.removeChild(links.firstChild);
	}
	var model = document.getElementById('link_template');
    var rerun = (current_link >= tracks.length ) || current_link < 0;
	tracks = [];
	for (var i=0; i<data.tokens.length; i++)
	{
        var token = data.tokens[i];
		tracks.push(token);
		var card = model.cloneNode(true);
		card.style.display = 'block';
		card.id = i.toString();
		card.getElementsByClassName('link_name')[0].innerHTML = token;
        if (i==current_link) {
            card.classList.add('bg-success');
            card.classList.remove('bg-secondary');
        }
		links.appendChild(card);

		links.append(document.createElement('br'));
	}
    if (rerun) {
        next();
    }
}
function loadLinks() {
	$.ajax({
		type: "get",
		url: get_url,
		async: true,
		data: {last_sync: last_sync},
		success: updateLinks
	})
}
