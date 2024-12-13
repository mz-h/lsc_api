import "./index.css";
import "./assets/styles/main.css";
import { createApp, reactive } from "vue";
import App from "./App.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import router from "./router/index.js";
import resourceManager from "../../libs/resourceManager";
// import call from "../../doppio/libs/controllers/call";
// import socket from "../../doppio/libs/controllers/socket";
// import Auth from "../../doppio/libs/controllers/auth";
// import socket from "../socket";

/* import the fontawesome core */
import { library, config } from "@fortawesome/fontawesome-svg-core";

/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";

library.add(fas, fab, far);

config.familyDefault = "classic";
config.styleDefault = "solid";

const app = createApp(App);
// const auth = reactive(new Auth());

// Plugins
app.component("font-awesome-icon", FontAwesomeIcon);
app.use(router);
app.use(resourceManager);
// Global Properties,
// components can inject this
// app.provide("$auth", auth);
// app.provide("$call", call);
// app.provide("$socket", socket);
app.component("VueDatePicker", VueDatePicker);
app.mount("#app");
