<template>
  <section
    :dir="$i18n.locale == 'ar' ? 'rtl' : 'ltr'"
    class="packages w-full px-4 min-h-screen lg:min-h-80 xl:min-h-screen flex flex-col justify-center items-center"
    id="packages"
  >
    <SectionTitle :title="t('Packages')" />
    <div
      class="pricing-cards flex flex-col place-content-center lg:flex-row gap-4 lg:flex-wrap"
    >
      <div
        class="pricing-card max-w-80 lg:min-w-80 flex flex-col justify-between gap-4 px-16 py-8 items-center bg-white rounded-md mt-8 hover:scale-105 duration-500"
      >
        <h3 class="text-2xl font-bold -mb-4">
          {{ $t("Golden.title") }}
        </h3>
        <h2 class="price text-4xl font-light">
          {{ $t("Golden.price") }}
        </h2>
        <p class="font-semibold text-2xl -mt-4">
          {{ $t("PackagesSection.SafeLife.duration") }}
        </p>
        <div class="price-notes flex flex-col gap-2 w-full text-center">
          <hr class="bg-white w-full" />
          <p>
            {{ $t("PackagesSection.SafeLife.lang") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("PackagesSection.SafeLife.languages") }}
            </span>
          </p>
                    <hr class="bg-white w-full" />
          <p>
            {{ $t("PackagesSection.General.cons") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("Golden.consultations") }}
            </span>
          </p>
                    <hr class="bg-white w-full" />
          <p>
            {{ $t("Golden.personalCase") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("Golden.personal") }}
            </span>
          </p>
                    <hr class="bg-white w-full" />
          <p>
            {{ $t("Golden.labCase") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("Golden.labor") }}
            </span>
          </p>

          <hr class="bg-white w-full" />
        </div>
        <div
          class="pri-btns flex flex-col gap-4 items-center justify-center w-full"
        >
          <a
            class="text-white font-bold py-2 px-4 rounded w-full btn bg-primary border-primary hover:bg-emerald-600 hover:border-emerald-600"
            href="https://portal.lsc-sa.net/dashboard/signup"
          >
            {{ $t("Subscribe") }}
          </a>
          <a
            class="text-white font-bold py-2 px-4 rounded w-1/2 btn bg-primary border-primary hover:bg-emerald-600 hover:border-emerald-600"
            href="https://portal.lsc-sa.net/dashboard"
          >
            {{ $t("Early Register") }}
          </a>
        </div>
      </div>
      <div
        class="pricing-card max-w-80 lg:min-w-80 flex flex-col justify-between gap-4 px-16 py-8 items-center bg-white rounded-md mt-8 hover:scale-105 duration-500"
      >
        <h3 class="text-2xl font-bold -mb-4">
          {{ $t("Silver.title") }}
        </h3>
        <h2 class="price text-4xl font-light">
          {{ $t("Silver.price") }}
        </h2>
        <p class="font-semibold text-2xl -mt-4">
          {{ $t("PackagesSection.SafeLife.duration") }}
        </p>
        <div class="price-notes flex flex-col gap-2 w-full text-center">
          <hr class="bg-white w-full" />
          <p>
            {{ $t("PackagesSection.SafeLife.lang") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("PackagesSection.SafeLife.languages") }}
            </span>
          </p>
                    <hr class="bg-white w-full" />
          <p>
            {{ $t("PackagesSection.General.cons") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("Silver.consultations") }}
            </span>
          </p>
                    <hr class="bg-white w-full" />
          <p>
            {{ $t("Silver.personalCase") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("Silver.personal") }}
            </span>
          </p>
                    <hr class="bg-white w-full" />
          <p>
            {{ $t("Silver.labCase") }}
            <span class="text-primary text-lg font-bold me-2">
              {{ $t("Silver.labor") }}
            </span>
          </p>

          <hr class="bg-white w-full" />
        </div>
        <div
          class="pri-btns flex flex-col gap-4 items-center justify-center w-full"
        >
          <a
            class="text-white font-bold py-2 px-4 rounded w-full btn bg-primary border-primary hover:bg-emerald-600 hover:border-emerald-600"
            href="https://portal.lsc-sa.net/dashboard/signup"
          >
            {{ $t("Subscribe") }}
          </a>
          <a
            class="text-white font-bold py-2 px-4 rounded w-1/2 btn bg-primary border-primary hover:bg-emerald-600 hover:border-emerald-600"
            href="https://portal.lsc-sa.net/dashboard"
          >
            {{ $t("Early Register") }}
          </a>
        </div>
      </div>
      <div
      class="pricing-card max-w-80 lg:min-w-80 flex flex-col justify-between gap-4 px-16 py-8 items-center bg-white rounded-md mt-8 hover:scale-105 duration-500"
    >
      <h3 class="text-2xl font-bold -mb-4">
        {{ $t("Bronze.title") }}
      </h3>
      <h2 class="price text-4xl font-light">
        {{ $t("Bronze.price") }}
      </h2>
      <p class="font-semibold text-2xl -mt-4">
        {{ $t("PackagesSection.SafeLife.duration") }}
      </p>
      <div class="price-notes flex flex-col gap-2 w-full text-center">
        <hr class="bg-white w-full" />
        <p>
          {{ $t("PackagesSection.SafeLife.lang") }}
          <span class="text-primary text-lg font-bold me-2">
            {{ $t("PackagesSection.SafeLife.languages") }}
          </span>
        </p>
                  <hr class="bg-white w-full" />
        <p>
          {{ $t("PackagesSection.General.cons") }}
          <span class="text-primary text-lg font-bold me-2">
            {{ $t("Bronze.consultations") }}
          </span>
        </p>
                  <hr class="bg-white w-full" />
        <p>
          {{ $t("Bronze.personalCase") }}
          <span class="text-primary text-lg font-bold me-2">
            {{ $t("Bronze.personal") }}
          </span>
        </p>
                  <hr class="bg-white w-full" />
        <p>
          {{ $t("Bronze.labCase") }}
          <span class="text-primary text-lg font-bold me-2">
            {{ $t("Bronze.labor") }}
          </span>
        </p>

        <hr class="bg-white w-full" />
      </div>
      <div
        class="pri-btns flex flex-col gap-4 items-center justify-center w-full"
      >
        <a
          class="text-white font-bold py-2 px-4 rounded w-full btn bg-primary border-primary hover:bg-emerald-600 hover:border-emerald-600"
          href="https://portal.lsc-sa.net/dashboard"
        >
          {{ $t("Subscribe") }}
        </a>
        <a
          class="text-white font-bold py-2 px-4 rounded w-1/2 btn bg-primary border-primary hover:bg-emerald-600 hover:border-emerald-600"
          href="https://portal.lsc-sa.net/dashboard"
        >
          {{ $t("Early Register") }}
        </a>
      </div>
    </div>
    </div>
  </section>
</template>

<style scoped>
.price {
  position: relative;
}
.price::before {
  /* content: "SAR"; */
  content: "";
  font-weight: 700;
  font-size: 16px;
  position: absolute;
  top: 0;
  left: -25%;
}
</style>

<script setup>
import SectionTitle from "./SectionTitle.vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>
