export default {
      clear() {
            // todo : implement
      },
      savePlayerName(playerName) {
            window.localStorage.setItem("playerName", playerName);
      },
      getPlayerName() {		
            return window.localStorage.getItem("playerName");
      },
      saveParticipationScore(participationScore) {
        window.localStorage.setItem("participationScore", participationScore);
      },
      getParticipationScore() {
        return window.localStorage.getItem("participationScore");
      },
      saveSize(size) {
            window.localStorage.setItem("size", size);
      },
      getSize() {
            return window.localStorage.getItem("size");
      }
    };