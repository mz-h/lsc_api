<template>
  <LoggedInTopNav title="حالة الدفع" :backArrow="true" />
  <div
    class="flex flex-col sm:flex-row w-full px-6 gap-5 mt-24 lg:mt-40 pb-24 pay"
  >
    <div v-if="paidInvoices">
      <div
        class="openInv flex flex-col gap-4 mt-4 mb-4 overflow-y-scroll mx-4 lg:grid lg:grid-cols-3"
      >
        <div
          class="openInvCard flex flex-col gap-4 px-4 py-2 bg-white shadow-sm relative"
          v-for="(invoice, ind) in paidInvoices"
          :key="ind"
        >
          <h2 class="invCardType text-black">
            {{ invoice.item[0].item_name }}
          </h2>
          <ul class="leading-8 flex justify-between text-success">
            <div class="flex gap-2 items-center">
              <li>
                <p class="text-sm text-wrap">
                  {{ invoice.currency }}
                </p>
              </li>
              <li>
                <p class="text-md text-wrap text-success">
                  {{ invoice.total }}
                </p>
              </li>
            </div>
            <li>
              <p class="text-md text-wrap">
                {{ invoice.creation.split(" ")[0] }}
              </p>
            </li>
          </ul>
          <button @click="toggleView(ind)" class="btn bg-primary text-white">
            {{ visibleInvoices[ind] ? "إخفاء" : "عرض الفاتورة" }}
          </button>
          <div :class="visibleInvoices[ind] ? '' : 'hidden'">
            <RouterLink
              :to="{
                path: '/profile/allInvoices/AnewPrint',
                query: { invoice: invoice.print_format },
              }"
              target="_blank"
              class="btn btn-sm w-full bg-primary border-primary rounded h-8 text-white"
            >
              عرض
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    <div v-else>لا يوجد فواتير سابقة</div>
  </div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import Loader from "@/components/Loader.vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import BottomNav from "@/components/BottomNav.vue";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";

const loading = ref(false);
const paidInvoices = ref([]);
const visibleInvoices = ref({}); // This object will track the visibility of each invoice
const navigate = useRouter();
const requestOptions = {
  method: "GET",
  headers: { Cookie: document.cookie },
  redirect: "follow",
};

fetch("/api/method/frappe.auth.get_logged_user", requestOptions)
  .then((response) => {
    if (!response.ok) {
      throw new Error("You are not logged In");
    }
    return response.json();
  })
  .then()
  .catch(() => navigate.replace("/"));

async function getInvoices() {
  loading.value = true;
  try {
    const response = await fetch(
      `/api/method/lsc_api.lsc_api.get_paid_invoices.get_paid_invoices`
    );
    const data = await response.json();
    if (data.message.status == "success") {
      paidInvoices.value = data.message.data;
    } else {
      console.error("Failed to get invoices");
    }
  } catch (error) {
    console.log("error" + error);
  } finally {
    loading.value = false;
  }
}

// Function to toggle the visibility of a specific invoice
function toggleView(ind) {
  visibleInvoices.value[ind] = !visibleInvoices.value[ind];
}
onMounted(() => {
  getInvoices();
});
</script>
