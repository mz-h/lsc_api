<template>
  <LoggedInTopNav title="ادفع الان" :backArrow="true" />
  <div
    v-if="!selected"
    class="payme flex flex-col min-h-screen gap-4 overflow-y-scroll px-4 py-20"
  >
    <h2 class="text-black font-bold">اختر طريقة الدفع</h2>
    <div class="paymethodSelect">
      <div class="tapMethod flex justify-between items-center">
        <input type="radio" name="radio-1" class="radio" checked="checked" />
        <span class="text-black font-bold">Pay With Tap</span>
      </div>
    </div>
    <button class="btn btn-primary" @click="handlePaynow">ادفع الان</button>
  </div>
  <!-- <iframe
    v-else
    class="mb-20 h-[90vh]"
    id="checkoutIframe"
    width="100%"
    style="border: none"
    :src="selected"
  ></iframe> -->
  <Loader v-if="loading" />
  <BottomNav />
</template>
<script setup>
import BottomNav from "@/components/BottomNav.vue";
import Loader from "@/components/Loader.vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import { ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const loading = ref(false);
const route = useRoute();
const plan_name = route.query.plan_name || "";
const salesInvoiceName = ref("");

const selected = ref(null);

async function handlePlanSelecting(plan_name) {
  loading.value = true;
  try {
    const res = await axios.post(
      "/api/method/lsc_api.lsc_api.subscription_plan.subscription_plan.create_subscription",
      { data: { plan_name: plan_name } },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );
    salesInvoiceName.value = res.data.message.data.sales_invoice;
    loading.value = false;
  } catch (error) {
    loading.value = false;
    console.error("Error creating subscription:", error);
  }
}

async function handlePaynow() {
  loading.value = true;
  await handlePlanSelecting(plan_name);
  try {
    const res = await axios.post(
      "/api/method/lsc_api.lsc_api.subscription_plan.subscription_plan.pay_subscription",
      { data: { sales_invoice: salesInvoiceName.value } },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );
    selected.value = res.data.message.data.transaction.url;
    window.location.href = res.data.message.data.transaction.url;
    loading.value = false;
  } catch (error) {
    loading.value = false;
    console.error("Error creating payment:", error);
  }
}
</script>
