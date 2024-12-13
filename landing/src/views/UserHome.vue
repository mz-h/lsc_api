<template>
  <!-- <Notification /> -->
  <LoggedInTopNav title="الرئيسية" :backArrow="false" />
  <div class="services w-full px-6 gap-5 mt-24 lg:mt-40 sm:mt-32">
    <h2 class="services__heading font-bold text-black mb-2">الطلبات الحالية</h2>
    <div class="flex overflow-y-scroll scrollbar-hide gap-4">
      <div class="card bg-white text-primary-content">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <h3 class="card-title text-sm text-wrap">
              قضية أولى تابعة لقسم الاستشارات
            </h3>
          </div>
          <ul class="leading-8">
            <li>
              <p class="text-gray-500 text-sm text-wrap">
                المحامى الموكل : أحمد محمد راشد
              </p>
            </li>
          </ul>
        </div>
      </div>

      <div class="card bg-white text-primary-content">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <h3 class="card-title text-sm text-wrap">
              قضية أولى تابعة لقسم الاستشارات
            </h3>
          </div>
          <ul class="leading-8">
            <li>
              <p class="text-gray-500">المحامى الموكل : أحمد محمد راشد</p>
            </li>
          </ul>
        </div>
      </div>

      <div class="card bg-white text-primary-content">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <h3 class="card-title text-sm text-wrap">
              قضية أولى تابعة لقسم الاستشارات
            </h3>
          </div>
          <ul class="leading-8">
            <li>
              <p class="text-gray-500">المحامى الموكل : أحمد محمد راشد</p>
            </li>
          </ul>
        </div>
      </div>

      <div class="card bg-white text-primary-content">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <h3 class="card-title text-sm text-wrap">
              قضية أولى تابعة لقسم الاستشارات
            </h3>
          </div>
          <ul class="leading-8">
            <li>
              <p class="text-gray-500">المحامى الموكل : أحمد محمد راشد</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="services px-5 pt-10 pb-24 lg:pb-40 flex flex-col gap-3">
    <h2 class="services__heading font-bold text-black">الخدمات المتاحة</h2>
    <h3 class="services__sub-heading">حسب باقتك</h3>
    <div
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-4"
    >
      <div class="card bg-white text-primary-content max-w-1/2">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <i class="fa-solid fa-handshake"></i>
            <h3 class="card-title text-sm text-wrap">قسم الاستشارات</h3>
          </div>
          <ul class="pr-6 list-disc leading-8">
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
          </ul>
        </div>
      </div>

      <div class="card bg-white text-primary-content max-w-1/2">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <i class="fa-solid fa-handshake"></i>
            <h3 class="card-title text-sm text-wrap">قسم الاستشارات</h3>
          </div>
          <ul class="pr-6 list-disc leading-8">
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
          </ul>
        </div>
      </div>

      <div class="card bg-white text-primary-content">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <i class="fa-solid fa-handshake"></i>
            <h3 class="card-title text-sm text-wrap">قسم الاستشارات</h3>
          </div>
          <ul class="pr-6 list-disc leading-8">
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
          </ul>
        </div>
      </div>

      <div class="card bg-white text-primary-content">
        <div class="card-body">
          <div class="card__title flex flex-row gap-2 items-center min-w-40">
            <i class="fa-solid fa-handshake"></i>
            <h3 class="card-title text-sm text-wrap">قسم الاستشارات</h3>
          </div>
          <ul class="pr-6 list-disc leading-8">
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
            <li>جلسة استشارية حضورية</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <BottomNav />

</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import Notification from "../components/Notification.vue";
</script>

<style scoped></style>
