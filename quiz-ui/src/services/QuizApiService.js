import axios from "axios";

const instance = axios.create({
	baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    return this.call("get","questions?position="+position);
  },
  getQuestionById(id) {
    return this.call("get","questions/"+id);
  },
  postParticipation(data){
    return this.call("post", "participations", data = data);
  },
  postLogin(data){
    return this.call("post", "login", data = data);
  },
  postAddQuestion(data, token){
    return this.call("post", "questions", data = data, token = token);
  },
  updateQuestion(id,data, token){
    return this.call("put","questions/"+id, data = data, token = token);
  },
  deleteQuestion(id, token){
    return this.call("delete","questions/"+id, null,token);
  },
  deleteParticipation(token){
    return this.call("delete","participations/all",null,token);
  }
};