import api from "./api";

const prefix = "boxscores/";
const separator = "/";

export default {
  getTopTTFL() {
    return api().get(prefix + "topttfl");
  },
  getNightTopTTFL(year, month, day) {
    return api().get(
      prefix + "topttfl/" + year + separator + month + separator + day
    );
  },
  getNightAllTTFL(year, month, day) {
    return api().get(
      prefix + "allttfl/" + year + separator + month + separator + day
    );
  },
  getTTFLSeasonAverages() {
    return api().get(prefix + "avg/ttfl");
  }
};
