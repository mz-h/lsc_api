<template>
  <LoggedInTopNav title="إدارة الباقة" :backArrow="false" />
  <div class="pt-4 bg-[ghostwhite] flex flex-col gap-4">
    <div
      v-if="subscription"
      class="services px-6 gap-5 mt-20 lg:mt-40 sm:mt-32 bg-white mx-8 py-4 rounded-3xl shadow-mycard"
    >
      <table class="text-black w-full">
        <tbody>
          <tr>
            <td class="text-md text-start w-1/3 mb-2">الباقة الحالية:</td>
            <td class="mx-auto text-primary text-center">
              {{ subscription.subscription_plan }}
            </td>
          </tr>
          <tr>
            <td class="text-md text-start">السعر:</td>
            <td class="mx-auto text-primary text-center">
              {{ subscription.plan_fees }}
              ريال سعودي
            </td>
          </tr>
          <tr>
            <td class="text-md text-start">حالة الباقة:</td>
            <td class="mx-auto text-primary text-center">
              {{ subscription.status }}
            </td>
          </tr>
          <tr>
            <td class="text-md text-start">تاريخ الاشتراك:</td>
            <td class="mx-auto text-primary text-center">
              {{ subscription.invoice_start_date }}
            </td>
          </tr>
          <tr>
            <td class="text-md text-start">تاريخ انتهاء الاشتراك:</td>
            <td class="mx-auto text-danger text-center">
              {{ subscription.invoice_end_date }}
            </td>
          </tr>
        </tbody>
      </table>
      <RouterLink
        :to="{ name: 'PackagesView' }"
        class="text-end block text-success"
      >
        تجديد او تغيير الباقة ⩥
      </RouterLink>
    </div>
    <!-- All Services -->
    <div v-if="allServices" class="flex flex-wrap mx-8 justify-center gap-2">
      <div
        v-for="(serv, index) in allServices"
        :key="index"
        class="bg-white shadow-mycard p-4 text-center rounded-xl relative"
      >
        <font-awesome-icon
          v-if="
            !subscription.allowed_services.some((el) => el == serv.service_name)
          "
          :icon="['fas', 'lock']"
          class="absolute top-0 left-0 font-sm"
        />
        <span class="text-black">
          {{ serv.service_name }}
        </span>
      </div>
    </div>
    <div
      v-if="subscription"
      class="services px-6 gap-5 bg-white mx-8 py-4 mb-24 rounded-3xl shadow-mycard"
    >
      <div
        style="width: 100%; height: 300px"
        class="overflow-hidden rounded-3xl"
      >
        <ag-charts :options="chartOptions"></ag-charts>
      </div>
      <div
        class="cont flex w-full justify-between items-center max-w-96 mx-auto"
      >
        <div
          class="flex flex-col items-center justify-center gap-2 text-center"
        >
          <div
            class="radial-progress text-center"
            :style="`--value: 
            ${(
              (subscription.remaining_consultation_hrs /
                subscription.consultation_hrs) *
              100
            ).toFixed(2)}
          `"
            role="progressbar"
          >
            {{ subscription.consultation_hrs }} /
            {{ subscription.remaining_consultation_hrs }}
          </div>
          <span class="text-lg font-bold text-black"> الاستشارات </span>
        </div>
        <div
          class="flex flex-col items-center justify-center gap-2 text-center"
        >
          <div
            class="radial-progress text-center"
            :style="`--value: 
          ${(
            (subscription.remaining_cases_hrs / subscription.cases_hrs) *
            100
          ).toFixed(2)}
        `"
            role="progressbar"
          >
            {{ subscription.cases_hrs }} /
            {{ subscription.remaining_cases_hrs }}
          </div>
          <span class="text-lg font-bold text-black"> القضايا </span>
        </div>
        <div
          class="flex flex-col items-center justify-center gap-2 text-center"
        >
          <div
            class="radial-progress text-center"
            :style="`--value: 
            ${(
              (subscription.remaining_legal_services_hrs /
                subscription.legal_services_hrs) *
              100
            ).toFixed(2)}
          `"
            role="progressbar"
          >
            {{ subscription.legal_services_hrs }} /
            {{ subscription.remaining_legal_services_hrs }}
          </div>
          <span class="text-lg font-bold text-black"> الخدمات </span>
        </div>
      </div>
    </div>
    <div
      v-else
      class="services w-full px-6 gap-5 flex flex-col items-center justify-center"
    >
      <h2 class="services__heading font-bold text-gray-400 mb-2 lg:text-5xl">
        لا يوجد اشتراك
      </h2>
      <RouterLink :to="{ name: 'PackagesView' }">
        <button class="btn btn-primary text-white lg:btn-lg">اشترك الان</button>
      </RouterLink>
    </div>
  </div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue";
import Loader from "@/components/Loader.vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { ref, onMounted, watch, onBeforeUnmount, inject, reactive } from "vue";
import { notificationsState } from "../router/notificationsState";
import { AgCharts } from "ag-charts-vue3";

const remHours = ref("15");
const conHours = ref("20");
const chartOptions = ref({});
const loading = ref(false);
const navigate = useRouter();
const subscription = ref([]);
const router = useRouter();
const allServices = ref([]);

const markNotificationsAsViewed = () => {
  hasNewNotifications.value = false;
};

fetch("/api/method/frappe.auth.get_logged_user", {
  method: "GET",
  headers: { Cookie: document.cookie },
  redirect: "follow",
})
  .then((response) => {
    if (!response.ok) {
      throw new Error("You are not logged In");
    }
    return response.json();
  })
  .then()
  .catch(() => navigate.replace("/"));

const fetchServices = async () => {
  loading.value = true;
  const response = await fetch(
    "/api/method/lsc_api.lsc_api.get_allowed_services.get_allowed_services"
  );
  const data = await response.json();
  allServices.value = data.message.allowed_services.sort((a, b) =>
    a.service_name.localeCompare(b.service_name, "ar")
  );
  loading.value = false;
};

const fetchData = async () => {
  loading.value = true;
  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.subscription_plan.subscription_plan.get_subscription_status"
    );
    const data = await response.json();
    const val = data.message.data.subscription;
    if (val && val != "null") {
      loading.value = false;
      subscription.value = data.message.data.subscription;
      conHours.value = Math.abs(
        subscription.value.total_hours - subscription.value.remaining_hours
      );
      remHours.value = subscription.value.remaining_hours;
      chartOptions.value = {
        data: [
          {
            segment: "المستهلكة",
            value: parseInt(conHours.value),
          },
          {
            segment: "المتبقية",
            value: parseInt(remHours.value),
          },
        ],
        title: {
          text: data.message.data.subscription.subscription_plan,
          fontFamily: "Cairo",
          fontWeight: "bold",
        },
        subtitle: {
          enabled: true,
          text: `${subscription.value.total_hours} مجموع الساعات`,
          fontFamily: "Cairo",
        },
        legend: {
          pagination: {
            label: {
              fontFamily: "Cairo",
            },
          },
          item: {
            label: {
              fontFamily: "Cairo",
              fontWeight: "bold",
            },
          },
        },
        series: [
          {
            type: "pie",
            angleKey: "value",
            calloutLabelKey: "segment",
            sectorLabelKey: "value",
            fills: ["#981D20", "#5978B9"],
            sectorLabel: {
              color: "white",
              fontFamily: "Cairo",
              fontWeight: "bold",
            },
            tooltip: {
              enabled: false,
            },
          },
        ],
      };
    } else {
      loading.value = false;
      subscription.value = null;
    }
  } catch (error) {
    loading.value = false;
    console.error("Error fetching data:", error);
  }
};

// const goToCaseStudyDetail = (requestId) => {
//   router.push({
//     path: `/requests/requestDetails`,
//     query: { requestId: requestId },
//   });
// };

onMounted(() => {
  fetchData();
  fetchServices();
});
</script>
