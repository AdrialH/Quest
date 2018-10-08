//JS Functions
placeDmgText();


$('.btn-attack').click(function(e) {
  $('.btn-attack').attr('disabled','disabled');
  //Generate Player and Monster Hits
  var playerHit = generateAttack(25);
  var monHit = generateAttack(10);

  $('.player-dmg').text(playerHit)
  $('.monster-dmg').text(monHit)

  console.log('playerHit = ' + playerHit)
  console.log('monHit = ' + monHit)

  //get Current Position of Monster to stop our animation at
  var monPos = $('.monster').position();
  console.log('monPos.left: ' + monPos.left);

  //get Current Width of Monster to add to its left position to stop the animation at
  var monWidth = $('.monster').width();
  console.log('monWidth: ' + monWidth);

  //DEBUG
  //just verifying that we are calculating correctly
  console.log('total: ' + (monPos.left + monWidth))
  console.log('window width: ' + $(window).width())
  console.log('difference: ' + ($(window).width() - (monPos.left + monWidth)) )
  //DEBUG

  //Animation loop for Player to go Hit monster and reset then monster to follow same, also to update amount of red in the hp bar 
  
  $('.player').animate({ "left": monPos.left - monWidth }, "slow", function() {
    $('.player-dmg').addClass('dmg-text-player')
    updateHp($('#monster-hp-bar'), playerHit, $('#monster-hp').text(), 1000, $('#monster-hp'))
  }).animate({ "left": "0" }, "slow", function() {
    $('.monster-dmg').addClass('dmg-text-mon')
    animateMonster();

  });


  //function created for callback animation for monster to return attack to player
  function animateMonster() {
    $('.monster').animate({ "left": -(monPos.left - monWidth) }, "slow", function() {
      updateHp($('#player-hp-bar'), monHit, $('#player-hp').text(), 1000, $('#player-hp'))
    } ).animate({ "left": "0" }, "slow", function() {
      $('.player-dmg').removeClass('dmg-text-player')
      $('.monster-dmg').removeClass('dmg-text-mon')
      $('.btn-attack').removeAttr('disabled');
    });
  }


});

//Used to generate a player and monster attack
function generateAttack(num) {
  return Math.floor(Math.random() * (50 - 10) + (10 + num))
}

//function used to make sure our dmg text is always placed above or avatars
function placeDmgText() {
  var mon = $('.monster').position();
  var player = $('.player').position();
  $('.player-dmg').css({
    "top": mon.top - 34,
    "left": mon.left
  });
  $('.monster-dmg').css({
    "top": player.top - 34,
    "left": $('.player').width()
  });
}


//when the window is resized be sure to reposition the dmg texts
$(window).resize(function(e) {
  placeDmgText();
})


function updateHp(element, dmg, currentHp, maxHp, hpTextElement) {

  var newHp = currentHp - dmg;
  console.log(`New ${element.attr('id')} HP = ${newHp}`)

  var hpBarWidth = (newHp / maxHp) * 100
  console.log(`New Width = ${hpBarWidth}`)

  var stringedWidth = hpBarWidth.toString().concat('%')

  if (newHp < 0 && element.attr('id') == 'monster-hp-bar') {
    newHp = 0;
    stringedWidth = '0%';
    $('.overlay').addClass('show')
  }
  $(element).css({'width':  stringedWidth})
  $(hpTextElement).text(newHp)
}

$('.btn-win').click(function(e) {
  location.reload();
});






//END
