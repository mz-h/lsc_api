import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import PersonalinfoView from "../views/PersonalinfoView.vue";
import ResidentialinfoView from "../views/ResidentialinfoView.vue";
import AllInvoicesView from "../views/AllInvoicesView.vue";
import PaymentResponseView from "../views/PaymentResponseView.vue";
import NProfileView from "../views/NProfileView.vue";
import UserHome from "../views/UserHome.vue";
import RequestsView from "../views/RequestsView.vue";
import ServicesView from "../views/ServicesView.vue";
import PackagesView from "../views/PackagesView.vue";
import Paynow from "../views/Paynow.vue";
import NotificationsView from "../views/NotificationsView.vue";
import StudyCaseView from "../views/StudyCaseView.vue";
import CreateCaseView from "../views/CreateCaseView.vue";
import CreateConsultationView from "../views/CreateConsultationView.vue";
import LegalServiceView from "../views/LegalServiceView.vue";
import RequestFollowUp from "../views/RequestFollowUp.vue";
import RequestDetails from "../views/RequestDetails.vue";
import UserSettingsView from "../views/UserSettingsView.vue";
import PowerofAttView from "../views/PowerofAttView.vue";
import PrivacyPolicy from "../views/PrivacyPolicy.vue";
import TermsView from "../views/TermsView.vue";
import CurrentPackageView from "../views/CurrentPackageView.vue";
import AnewPrint from "../views/AnewPrint.vue";

const router = createRouter({
  base: "/dashboard/",
  history: createWebHistory("/dashboard"),
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
      path: "/profile/payRes",
      name: "PaymentResponseView",
      component: PaymentResponseView,
    },
    {
      path: "/profile/privacypolicy",
      name: "PrivacyPolicy",
      component: PrivacyPolicy,
    },
    {
      path: "/profile/termsofuse",
      name: "TermsView",
      component: TermsView,
    },
    {
      path: "/profile/residentialInfo",
      name: "ResidentialinfoView",
      component: ResidentialinfoView,
    },
    {
      path: "/profile/allInvoices",
      name: "AllInvoicesView",
      component: AllInvoicesView,
    },
    {
      path: "/profile/allInvoices/AnewPrint",
      name: "AnewPrint",
      component: AnewPrint,
    },
    {
      path: "/profile/personaldetails",
      name: "PersonalinfoView",
      component: PersonalinfoView,
    },
    {
      path: "/profile/CurrentPackage",
      name: "CurrentPackageView",
      component: CurrentPackageView,
    },
    {
      path: "/profile/account",
      name: "UserSettingsView",
      component: UserSettingsView,
    },
    {
      path: "/profile/attorney",
      name: "PowerofAttView",
      component: PowerofAttView,
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
      path: "/requests/requestDetails",
      name: "RequestDetails",
      component: RequestDetails,
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
    },
    {
      path: "/packages/paynow",
      name: "Paynow",
      component: Paynow,
    },
    {
      path: "/notifications",
      name: "Notifications",
      component: NotificationsView,
    },
    {
      path: "/services/study-case",
      name: "StudyCaseView",
      component: StudyCaseView,
    },
    {
      path: "/services/legal",
      name: "LegalServiceView",
      component: LegalServiceView,
    },
    {
      path: "/services/case",
      name: "CreateCaseView",
      component: CreateCaseView,
    },
    {
      path: "/services/consultation",
      name: "CreateConsultationView",
      component: CreateConsultationView,
    },
    {
      path: "/study-case-read/:id",
      name: "RequestFollowUp",
      component: RequestFollowUp,
      props: true,
    },
  ],
});

export default router;
