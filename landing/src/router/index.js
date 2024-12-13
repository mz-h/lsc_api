import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import OLDProfileView from "../views/OLDProfileView.vue";
import NProfileView from "../views/NProfileView.vue";
import UserHome from "../views/UserHome.vue";
import RequestsView from "../views/RequestsView.vue";
import ServicesView from "../views/ServicesView.vue";
import PackagesView from "../views/PackagesView.vue";
import RequestDetails from "../views/RequestDetails.vue";

const router = createRouter({
  base: "/landing/",
  history: createWebHistory("/landing"),
  routes: [
    {
      path: "/",
      name: "login",
      component: LoginView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
    },
    {
      path: "/profile/details",
      name: "OLDProfileView",
      component: OLDProfileView,
    },
    {
      path: "/profile",
      name: "NProfileView",
      component: NProfileView,
    },
    {
      path: "/home",
      name: "userhome",
      component: UserHome,
    },
    {
      path: "/requests",
      name: "RequestsView",
      component: RequestsView,
    },
    {
      path: '/request/:id',
      name: 'RequestDetails',
      component: RequestDetails,
      props: true
    },
  
    {
      path: "/services",
      name: "ServicesView",
      component: ServicesView,
    },
    {
      path: "/packages",
      name: "PackagesView",
      component: PackagesView,
    }
  ],
});

export default router;
