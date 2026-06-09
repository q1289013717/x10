<template>
  <AppLayout current-page="calendar" :show-back="false">
    <!-- ====== Calendar 自定义 Header ====== -->
      <!-- 顶部导航 -->
      <header class="bg-white/80 backdrop-blur-xl border-b border-slate-100 px-4 py-4 lg:px-6 sticky top-0 z-40">
        <div class="flex items-center justify-between max-w-[1600px] mx-auto">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
                <span class="text-white text-lg">📋</span>
              </div>
              <div>
                <h1 class="font-bold text-slate-900 text-xl tracking-tight">X10成长日程</h1>
                <p class="text-xs text-slate-500 cursor-pointer" @click="editingCompany = true">
                  {{ companyName }}
                </p>
                <input
                  v-if="editingCompany"
                  ref="companyInput"
                  v-model="companyName"
                  class="text-xs border rounded px-1 py-0.5"
                  @blur="saveCompanyName"
                  @keyup.enter="saveCompanyName"
                />
              </div>
            </div>
          </div>

          <div class="flex items-center gap-3 flex-1 min-w-0">
            <!-- 视图切换 -->
            <div class="hidden md:flex items-center gap-1 bg-slate-100 rounded-xl p-1 flex-shrink-0">
              <button
                v-for="v in views"
                :key="v.key"
                @click="viewMode = v.key"
                :class="[
                  'px-3 py-1.5 rounded-lg transition-all duration-200 text-sm font-medium',
                  viewMode === v.key ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-800'
                ]"
              >{{ v.label }}</button>
            </div>
            <div class="flex md:hidden items-center gap-1 bg-slate-100 rounded-lg p-1 flex-shrink-0">
              <button
                v-for="v in views"
                :key="v.key"
                @click="viewMode = v.key"
                :class="[
                  'px-2 py-1 rounded-lg text-xs transition-all',
                  viewMode === v.key ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600'
                ]"
              >{{ v.label }}</button>
            </div>

            <div class="flex-1" />

            <router-link to="/settings" class="p-2 hover:bg-slate-100 rounded-xl">
              <span class="text-slate-600 text-lg">⚙</span>
            </router-link>
          </div>
        </div>
      </header>

      <!-- 统计卡片 -->
      <div class="bg-gradient-to-b from-white to-[#f5f6f7] border-b border-slate-100 px-4 py-5 lg:px-6">
        <div class="max-w-[1600px] mx-auto">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-gradient-to-br from-blue-500 via-blue-600 to-blue-700 rounded-2xl p-5 shadow-lg shadow-blue-500/20 relative overflow-hidden">
              <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
              <div class="relative">
                <div class="flex items-center gap-3 mb-3">
                  <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                    <span class="text-white text-sm">🎯</span>
                  </div>
                  <span class="text-sm font-medium text-blue-100">目标营业额</span>
                </div>
                <p class="text-2xl font-bold text-white tracking-tight">¥{{ (monthlyStats.totalTarget / 10000).toFixed(1) }}万</p>
              </div>
            </div>
            <div class="bg-gradient-to-br from-emerald-500 via-emerald-600 to-teal-600 rounded-2xl p-5 shadow-lg shadow-emerald-500/20 relative overflow-hidden">
              <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
              <div class="relative">
                <div class="flex items-center gap-3 mb-3">
                  <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                    <span class="text-white text-sm">📈</span>
                  </div>
                  <span class="text-sm font-medium text-emerald-100">已完成</span>
                </div>
                <p class="text-2xl font-bold text-white tracking-tight">¥{{ (monthlyStats.totalCompleted / 10000).toFixed(1) }}万</p>
              </div>
            </div>
            <div class="bg-gradient-to-br from-cyan-500 via-cyan-600 to-blue-600 rounded-2xl p-5 shadow-lg shadow-cyan-500/20 relative overflow-hidden">
              <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
              <div class="relative">
                <div class="flex items-center gap-3 mb-3">
                  <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                    <span class="text-white text-sm">📊</span>
                  </div>
                  <span class="text-sm font-medium text-cyan-100">完成率</span>
                </div>
                <p class="text-2xl font-bold text-white tracking-tight">{{ completionRate }}%</p>
                <div class="mt-3 h-2 bg-white/20 rounded-full overflow-hidden">
                  <div class="h-full bg-white rounded-full transition-all duration-500" :style="{ width: completionRate + '%' }" />
                </div>
              </div>
            </div>
            <div class="bg-gradient-to-br from-amber-500 via-orange-500 to-amber-600 rounded-2xl p-5 shadow-lg shadow-amber-500/20 relative overflow-hidden">
              <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
              <div class="relative">
                <div class="flex items-center gap-3 mb-3">
                  <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
                    <span class="text-white text-sm">👥</span>
                  </div>
                  <span class="text-sm font-medium text-amber-100">任务数</span>
                </div>
                <p class="text-2xl font-bold text-white tracking-tight">{{ monthlyStats.totalTasks }}个</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 日历控制栏 -->
      <div class="bg-white border-b border-slate-100 px-4 py-4 lg:px-6">
        <div class="max-w-[1600px] mx-auto flex items-center justify-between">
          <div class="flex items-center gap-3">
            <button @click="navigate(-1)" class="p-2 border border-slate-200 rounded-xl hover:bg-slate-50">
              <span class="text-slate-600">←</span>
            </button>
            <h2 class="text-xl font-bold text-slate-900 tracking-tight">{{ viewTitle }}</h2>
            <button @click="navigate(1)" class="p-2 border border-slate-200 rounded-xl hover:bg-slate-50">
              <span class="text-slate-600">→</span>
            </button>
          </div>
          <button @click="goToToday" class="px-4 py-2 border border-slate-200 rounded-xl hover:bg-slate-50 text-slate-700 text-sm">
            今天
          </button>
        </div>
      </div>

      <!-- 视图内容 -->
      <div class="flex-1 overflow-auto p-4 lg:p-6">
        <div class="max-w-[1600px] mx-auto">
          <!-- 月视图 -->
          <div v-if="viewMode === 'month'" class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="grid grid-cols-7 border-b border-slate-100 bg-gradient-to-b from-slate-50 to-white">
              <div v-for="(d, i) in weekDays" :key="i" :class="['py-4 text-center font-semibold text-sm', i === 0 || i === 6 ? 'text-slate-500' : 'text-slate-600']">
                {{ d }}
              </div>
            </div>
            <div class="grid grid-cols-7">
              <div
                v-for="(day, index) in monthDays"
                :key="index"
                :class="[
                  'min-h-[120px] md:min-h-[140px] border-b border-r border-slate-100 p-3 relative group cursor-pointer transition-all duration-200',
                  day ? getDayClasses(day) : 'bg-slate-50/30 border-slate-50'
                ]"
                @click="day && tasks[getDateKey(day)] && viewTaskDetail(day)"
                @dragover.prevent="handleDragOver($event, day ? getDateKey(day) : '')"
                @dragleave="handleDragLeave"
                @drop="handleDrop($event, day ? getDateKey(day) : '')"
              >
                <template v-if="day">
                  <div class="flex items-center justify-between mb-2">
                    <span :class="getDayNumberClasses(day)">
                      {{ day }}
                    </span>
                    <button
                      class="w-7 h-7 opacity-0 group-hover:opacity-100 transition-all duration-200 hover:bg-blue-50 rounded-xl flex items-center justify-center"
                      @click.stop="addTask(day)"
                    >
                      <span class="text-blue-500 text-sm">+</span>
                    </button>
                  </div>
                  <div v-if="getDayData(day)" class="space-y-2">
                    <div class="flex items-center gap-2">
                      <div :class="['h-2 rounded-full transition-all duration-300 flex-1', getStatusColor(getDayData(day))]" :style="{ width: getDayProgress(getDayData(day)) + '%' }" />
                      <span class="text-[12px] text-gray-500">{{ Math.round(getDayProgress(getDayData(day))) }}%</span>
                    </div>
                    <div class="flex items-center gap-1.5 text-xs">
                      <span class="font-medium text-slate-600">¥{{ ((getDayData(day).completedAmount || 0) / 1000).toFixed(0) }}k</span>
                      <span class="text-slate-300">/</span>
                      <span class="text-slate-400">¥{{ ((getDayData(day).targetAmount || 0) / 1000).toFixed(0) }}k</span>
                    </div>
                    <div v-if="hasRisk(getDayData(day))" class="flex items-center gap-1">
                      <span class="text-amber-500 text-xs">⚠</span>
                      <span class="text-xs font-medium text-amber-600">有风险</span>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>

          <!-- 周视图 -->
          <div v-if="viewMode === 'week'" class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="grid grid-cols-7 border-b border-slate-100 bg-gradient-to-b from-slate-50 to-white">
              <div
                v-for="(d, i) in weekDates"
                :key="i"
                :class="['py-4 text-center border-r border-slate-100 last:border-r-0', i === 0 || i === 6 ? 'bg-slate-50/50' : '', isTodayDate(d) ? 'bg-blue-50' : '']"
              >
                <div :class="['text-sm font-semibold', isTodayDate(d) ? 'text-blue-600' : 'text-slate-600']">{{ weekDays[i] }}</div>
                <div :class="['text-xl font-bold mt-1', isTodayDate(d) ? 'text-blue-600' : 'text-slate-900']">{{ d.getDate() }}</div>
              </div>
            </div>
            <div class="grid grid-cols-7 min-h-[450px]">
              <div
                v-for="(d, i) in weekDates"
                :key="i"
                :class="[
                  'border-r border-slate-100 last:border-r-0 p-4 min-h-[450px]',
                  i === 0 || i === 6 ? 'bg-slate-50/30' : '',
                  isTodayDate(d) ? 'bg-blue-50/30' : '',
                  dragOverDate === getDateKeyFromDate(d) ? 'bg-blue-100 ring-2 ring-blue-400' : ''
                ]"
                @dragover.prevent="handleDragOver($event, getDateKeyFromDate(d))"
                @dragleave="handleDragLeave"
                @drop="handleDrop($event, getDateKeyFromDate(d))"
              >
                <button
                  class="w-full mb-3 opacity-0 hover:opacity-100 transition-all duration-200 rounded-xl hover:bg-blue-50 text-blue-600 text-sm py-1.5"
                  @click="addTask(d.getDate())"
                >+ 添加</button>
                <div v-if="getDayDataRaw(getDateKeyFromDate(d))" class="space-y-2.5">
                  <div
                    v-for="task in getDayDataRaw(getDateKeyFromDate(d)).tasks"
                    :key="task.id"
                    class="bg-white rounded-xl p-3 shadow-sm border border-slate-100 cursor-move hover:shadow-md hover:border-slate-200 transition-all duration-200"
                    draggable="true"
                    @dragstart="handleDragStart($event, task, getDateKeyFromDate(d))"
                  >
                    <div class="flex items-start gap-2">
                      <span class="text-slate-300 text-xs mt-0.5 flex-shrink-0">⋮⋮</span>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-slate-800 truncate">{{ task.title || task.action || '未命名' }}</p>
                        <p v-if="task.responsible" class="text-xs text-slate-500 mt-1.5 flex items-center gap-1">👤 {{ task.responsible }}</p>
                        <p v-if="task.risk && task.risk !== '无'" class="text-xs text-amber-600 mt-1.5 bg-amber-50 rounded-lg p-1.5">⚠ {{ task.risk }}</p>
                      </div>
                      <div class="relative" @click.stop>
                        <button class="w-7 h-7 hover:bg-slate-100 rounded-lg text-slate-400 text-xs" @click="toggleTaskMenu(task, getDateKeyFromDate(d))">⋯</button>
                        <div v-if="openMenuId === task.id" class="absolute right-0 top-full mt-1 bg-white rounded-xl shadow-lg border border-slate-100 py-1 z-10 min-w-[100px]">
                          <button class="w-full text-left px-3 py-2 text-sm hover:bg-slate-50" @click="editTask(getDateKeyFromDate(d), task)">编辑</button>
                          <button class="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50" @click="deleteTaskFromMenu(getDateKeyFromDate(d), task)">删除</button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="mt-4 pt-3 border-t border-slate-100">
                    <div class="flex items-center justify-between text-xs mb-2">
                      <span class="text-slate-500">完成度</span>
                      <span class="font-semibold text-slate-700">{{ Math.round(getDayProgress(getDayDataRaw(getDateKeyFromDate(d)))) }}%</span>
                    </div>
                    <div :class="['h-2 rounded-full', getStatusColor(getDayDataRaw(getDateKeyFromDate(d)))]" :style="{ width: getDayProgress(getDayDataRaw(getDateKeyFromDate(d))) + '%' }" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 日视图 -->
          <div v-if="viewMode === 'day'" class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="p-6 lg:p-8">
              <div class="flex items-center justify-between mb-8">
                <div>
                  <h3 class="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
                    {{ currentDate.getFullYear() }}年{{ currentDate.getMonth() + 1 }}月{{ currentDate.getDate() }}日
                  </h3>
                  <p class="text-slate-500 mt-2">{{ weekDays[currentDate.getDay()] }}</p>
                </div>
                <button @click="addTask(currentDate.getDate())" class="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-xl shadow-lg shadow-blue-500/30 px-5 py-2.5 text-sm font-medium transition-all">
                  + 添加任务
                </button>
              </div>

              <div v-if="!dayViewData || !dayViewData.tasks || dayViewData.tasks.length === 0" class="text-center py-16 text-slate-400">
                <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
                  <span class="text-4xl">📅</span>
                </div>
                <p class="text-lg text-slate-600 font-medium mb-2">今日暂无任务</p>
                <p class="text-slate-400 mb-6">点击下方按钮添加第一个任务</p>
                <button @click="addTask(currentDate.getDate())" class="px-5 py-2.5 border border-slate-200 rounded-xl hover:bg-slate-50">添加第一个任务</button>
              </div>

              <div v-else class="space-y-8">
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 text-center">
                    <p class="text-sm text-slate-600 mb-2 font-medium">目标营业额</p>
                    <p class="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">¥{{ ((dayViewData.targetAmount || 0) / 10000).toFixed(1) }}万</p>
                  </div>
                  <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-2xl p-6 text-center">
                    <p class="text-sm text-slate-600 mb-2 font-medium">已完成</p>
                    <p class="text-2xl lg:text-3xl font-bold text-emerald-600 tracking-tight">¥{{ ((dayViewData.completedAmount || 0) / 10000).toFixed(1) }}万</p>
                  </div>
                  <div class="bg-gradient-to-br from-cyan-50 to-cyan-100 rounded-2xl p-6 text-center">
                    <p class="text-sm text-slate-600 mb-2 font-medium">完成率</p>
                    <p class="text-2xl lg:text-3xl font-bold text-cyan-600 tracking-tight">{{ dayViewProgress }}%</p>
                  </div>
                </div>

                <div class="bg-gradient-to-br from-slate-50 to-white rounded-2xl p-6 border border-slate-100">
                  <div class="flex items-center justify-between text-sm mb-3">
                    <span class="text-slate-600 font-medium">完成进度</span>
                    <span class="font-semibold text-slate-900">{{ dayViewProgress }}%</span>
                  </div>
                  <div class="h-3 bg-slate-200 rounded-full overflow-hidden">
                    <div class="h-full bg-blue-500 rounded-full transition-all duration-500" :style="{ width: dayViewProgress + '%' }" />
                  </div>
                </div>

                <div>
                  <h4 class="font-semibold text-slate-900 mb-5 text-lg flex items-center gap-2">
                    <div class="w-1 h-5 bg-blue-500 rounded-full" />
                    今日任务 ({{ dayViewData.tasks.length }}个)
                  </h4>
                  <div class="space-y-4">
                    <div v-for="(task, idx) in dayViewData.tasks" :key="task.id" class="bg-slate-50/70 rounded-2xl p-5 flex items-start gap-4 border border-slate-100">
                      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 text-white flex items-center justify-center font-bold text-lg flex-shrink-0 shadow-lg shadow-blue-500/30">
                        {{ Number(idx) + 1 }}
                      </div>
                      <div class="flex-1 min-w-0">
                        <div class="flex items-start justify-between gap-4">
                          <h5 class="font-semibold text-slate-900 text-base">{{ task.title || task.action || '未命名' }}</h5>
                          <div class="flex items-center gap-2 flex-shrink-0">
                            <span v-if="task.risk && task.risk !== '无'" class="bg-amber-100 text-amber-700 rounded-lg px-3 py-1 text-xs flex items-center gap-1">
                              ⚠ 风险
                            </span>
                            <button class="w-8 h-8 rounded-xl hover:bg-slate-200 flex items-center justify-center text-slate-600" @click="toggleDayTaskMenu(task)">⋯</button>
                            <div v-if="dayTaskMenuId === task.id" class="absolute right-4 mt-2 bg-white rounded-xl shadow-lg border border-slate-100 py-1 z-10">
                              <button class="w-full text-left px-3 py-2 text-sm hover:bg-slate-50" @click="editDayTask(task)">编辑</button>
                              <button class="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50" @click="deleteDayTask(task)">删除</button>
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-5 mt-3 text-sm text-slate-600">
                          <span v-if="task.responsible" class="flex items-center gap-2">👤 负责人: <span class="font-medium text-slate-700">{{ task.responsible }}</span></span>
                        </div>
                        <p v-if="task.risk && task.risk !== '无'" class="mt-3 text-sm text-amber-700 bg-amber-50 rounded-xl p-3 border border-amber-100">
                          <span class="font-medium">风险备注:</span> {{ task.risk }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    <!-- 任务详情弹窗 -->
    <Teleport to="body">
      <div v-if="selectedDate" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="closeDetail">
        <div class="bg-white rounded-2xl max-w-lg w-full max-h-[85vh] overflow-auto shadow-2xl">
          <div class="p-6 lg:p-8">
            <div class="flex items-center justify-between mb-8">
              <h3 class="text-xl font-bold text-slate-900 tracking-tight">{{ selectedDate.dateKey }} 任务详情</h3>
              <button @click="closeDetail" class="p-2 hover:bg-slate-100 rounded-xl">
                <span class="text-slate-500 text-lg">✕</span>
              </button>
            </div>

            <div class="space-y-4 mb-8">
              <div class="bg-gradient-to-br from-slate-50 to-white rounded-2xl p-5 border border-slate-100">
                <div class="flex items-center justify-between mb-3">
                  <span class="text-sm font-medium text-slate-600">目标营业额</span>
                  <span class="font-semibold text-slate-900 text-lg">¥{{ (selectedDate.targetAmount || 0).toLocaleString() }}</span>
                </div>
                <div class="flex items-center justify-between mb-3">
                  <span class="text-sm font-medium text-slate-600">已完成</span>
                  <span class="font-semibold text-emerald-600 text-lg">¥{{ (selectedDate.completedAmount || 0).toLocaleString() }}</span>
                </div>
                <div class="flex items-center justify-between mb-4">
                  <span class="text-sm font-medium text-slate-600">完成率</span>
                  <span class="font-semibold text-blue-600 text-lg">{{ detailProgress }}%</span>
                </div>
                <div class="h-2.5 bg-slate-200 rounded-full overflow-hidden">
                  <div class="h-full bg-blue-500 rounded-full" :style="{ width: detailProgress + '%' }" />
                </div>
              </div>
            </div>

            <h4 class="font-semibold text-slate-900 mb-4 text-lg flex items-center gap-2">
              <div class="w-1 h-5 bg-blue-500 rounded-full" />
              当日任务
            </h4>
            <div class="space-y-3.5">
              <div v-for="task in selectedDate.tasks" :key="task.id" class="bg-slate-50 rounded-xl p-4 border border-slate-100">
                <div class="flex items-start justify-between mb-2">
                  <span class="font-medium text-slate-800">{{ task.title || task.action || '未命名' }}</span>
                  <span v-if="task.risk && task.risk !== '无'" class="bg-amber-100 text-amber-700 rounded-lg px-2 py-1 text-xs flex items-center gap-1">⚠ 风险</span>
                </div>
                <div v-if="task.responsible" class="text-sm text-slate-600 flex items-center gap-1">👤 {{ task.responsible }}</div>
                <p v-if="task.risk && task.risk !== '无'" class="mt-3 text-sm text-amber-600 bg-amber-50 rounded-lg p-2.5">风险备注: {{ task.risk }}</p>
              </div>
            </div>

            <div class="mt-8 flex gap-3">
              <button @click="editSelectedDate" class="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-xl shadow-lg shadow-blue-500/30 px-4 py-2.5 text-sm font-medium transition-all">编辑任务</button>
              <button @click="closeDetail" class="flex-1 border border-slate-200 rounded-xl hover:bg-slate-50 px-4 py-2.5 text-sm">关闭</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Toast 通知 -->
    <Teleport to="body">
      <div v-if="toast.show" class="fixed top-4 right-4 z-[100] bg-white rounded-xl shadow-lg border border-slate-100 px-5 py-3 animate-[fade-in_0.3s_ease-out]">
        <p class="font-semibold text-slate-900 text-sm">{{ toast.title }}</p>
        <p class="text-slate-500 text-xs mt-1">{{ toast.desc }}</p>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/tasks'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const router = useRouter()
const taskStore = useTaskStore()
const authStore = useAuthStore()

// 响应式状态
const currentDate = ref(new Date())
const viewMode = ref('month')
const tasks = ref<Record<string, any>>({})
const selectedDate = ref<any>(null)
const draggedTask = ref<any>(null)
const dragOverDate = ref('')
const companyName = ref('涌动花鱼科技有限公司')
const editingCompany = ref(false)
const companyInput = ref<HTMLInputElement | null>(null)

// 菜单状态
const openMenuId = ref<number | string | null>(null)
const dayTaskMenuId = ref<number | string | null>(null)

// Toast
const toast = reactive({ show: false, title: '', desc: '' })
let toastTimer: ReturnType<typeof setTimeout> | null = null
function showToast(title: string, desc: string) {
  toast.title = title; toast.desc = desc; toast.show = true
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.show = false }, 2500)
}

// 常量
const weekDays = ['日', '一', '二', '三', '四', '五', '六']
const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
const views = [
  { key: 'month', label: '月' },
  { key: 'week', label: '周' },
  { key: 'day', label: '日' }
]

// 计算属性 - 视图标题
const viewTitle = computed(() => {
  const y = currentDate.value.getFullYear()
  const m = currentDate.value.getMonth()
  const d = currentDate.value.getDate()
  if (viewMode.value === 'month') return `${y}年 ${monthNames[m]}`
  if (viewMode.value === 'week') return `${y}年 第${Math.ceil((d + new Date(y, m, 1).getDay()) / 7)}周`
  return `${y}年${monthNames[m]}${d}日`
})

// 计算月份天数网格
const monthDays = computed(() => {
  const y = currentDate.value.getFullYear()
  const m = currentDate.value.getMonth()
  const firstDay = new Date(y, m, 1).getDay()
  const lastDay = new Date(y, m + 1, 0).getDate()
  const days: (number | null)[] = []
  for (let i = 0; i < firstDay; i++) days.push(null)
  for (let i = 1; i <= lastDay; i++) days.push(i)
  return days
})

// 周视图日期
const weekDates = computed(() => {
  const d = new Date(currentDate.value)
  const day = d.getDay()
  d.setDate(d.getDate() - day)
  const dates: Date[] = []
  for (let i = 0; i < 7; i++) {
    const nd = new Date(d)
    nd.setDate(d.getDate() + i)
    dates.push(nd)
  }
  return dates
})

// 日视图数据
const dayViewData = computed(() => {
  const dk = formatDateKey(currentDate.value.getFullYear(), currentDate.value.getMonth(), currentDate.value.getDate())
  return tasks.value[dk] || null
})

const dayViewProgress = computed(() => {
  if (!dayViewData.value) return 0
  const d = dayViewData.value
  return d.targetAmount > 0 ? Math.round((d.completedAmount || 0) / d.targetAmount * 100) : 0
})

// 月度统计
const monthlyStats = computed(() => {
  const data = tasks.value
  let totalTarget = 0, totalCompleted = 0, totalTasks = 0
  const y = currentDate.value.getFullYear()
  const m = currentDate.value.getMonth()
  Object.entries(data).forEach(([key, day]: [string, any]) => {
    const [yy, mm] = key.split('-').map(Number)
    if (yy === y && mm === m + 1) {
      totalTarget += day.targetAmount || 0
      totalCompleted += day.completedAmount || 0
      totalTasks += (day.tasks || []).length
    }
  })
  return { totalTarget, totalCompleted, totalTasks }
})

const completionRate = computed(() => {
  return monthlyStats.value.totalTarget > 0 ? Math.round(monthlyStats.value.totalCompleted / monthlyStats.value.totalTarget * 100) : 0
})

const detailProgress = computed(() => {
  if (!selectedDate.value) return 0
  const t = selectedDate.value.targetAmount || 0
  const c = selectedDate.value.completedAmount || 0
  return t > 0 ? Math.round(c / t * 100) : 0
})

// 工具函数
function formatDateKey(y: number, m: number, d: number) {
  return `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`
}

function getDateKey(day: number) {
  return formatDateKey(currentDate.value.getFullYear(), currentDate.value.getMonth(), day)
}

function getDateKeyFromDate(d: Date) {
  return formatDateKey(d.getFullYear(), d.getMonth(), d.getDate())
}

function getDayData(day: number) {
  return tasks.value[getDateKey(day)]
}

function getDayDataRaw(dateKey: string) {
  return tasks.value[dateKey]
}

function getDayProgress(dayData: any) {
  if (!dayData || !dayData.targetAmount) return 0
  return Math.min((dayData.completedAmount || 0) / dayData.targetAmount * 100, 100)
}

function getStatusColor(dayData: any) {
  const pct = getDayProgress(dayData)
  if (pct >= 100) return 'bg-emerald-500'
  if (pct >= 70) return 'bg-cyan-500'
  if (pct >= 40) return 'bg-amber-500'
  return 'bg-red-500'
}

function hasRisk(dayData: any) {
  return dayData?.tasks?.some((t: any) => t.risk && t.risk !== '无')
}

function isTodayDate(date: Date) {
  return new Date().toDateString() === date.toDateString()
}

function getDayClasses(day: number) {
  const cls = []
  if (isToday(day)) cls.push('bg-blue-50/50')
  else cls.push('hover:bg-slate-50')
  if (dragOverDate.value === getDateKey(day)) cls.push('bg-blue-100 ring-2 ring-blue-400')
  return cls.join(' ')
}

function getDayNumberClasses(day: number) {
  return [
    'text-sm font-semibold w-8 h-8 flex items-center justify-center rounded-full transition-all',
    isToday(day) ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-md shadow-blue-500/30' : 'text-slate-700 hover:bg-slate-100'
  ].join(' ')
}

function isToday(day: number) {
  return new Date().toDateString() === new Date(currentDate.value.getFullYear(), currentDate.value.getMonth(), day).toDateString()
}

// 导航
function navigate(dir: number) {
  const d = new Date(currentDate.value)
  if (viewMode.value === 'month') d.setMonth(d.getMonth() + dir)
  else if (viewMode.value === 'week') d.setDate(d.getDate() + dir * 7)
  else d.setDate(d.getDate() + dir)
  currentDate.value = d
}

function goToToday() {
  currentDate.value = new Date()
}

// 任务操作
function addTask(day: number) {
  const dk = getDateKey(day)
  router.push({ path: '/task-edit', query: { date: dk } })
}

function viewTaskDetail(day: number) {
  const dk = getDateKey(day)
  const dayTasks = tasks.value[dk]
  if (dayTasks) {
    selectedDate.value = { day, dateKey: dk, ...dayTasks }
  }
}

function closeDetail() {
  selectedDate.value = null
}

function editSelectedDate() {
  if (selectedDate.value) {
    const dk = selectedDate.value.dateKey
    closeDetail()
    router.push({ path: '/task-edit', query: { date: dk } })
  }
}

function editTask(dateKey: string, task: any) {
  openMenuId.value = null
  router.push({ path: '/task-edit', query: { date: dateKey, taskId: String(task.id) } })
}

function editDayTask(task: any) {
  dayTaskMenuId.value = null
  const dk = formatDateKey(currentDate.value.getFullYear(), currentDate.value.getMonth(), currentDate.value.getDate())
  router.push({ path: '/task-edit', query: { date: dk, taskId: String(task.id) } })
}

async function deleteTaskFromMenu(dateKey: string, task: any) {
  openMenuId.value = null
  try {
    await taskStore.deleteTask(dateKey, task.id)
    tasks.value[dateKey].tasks = tasks.value[dateKey].tasks.filter((t: any) => t.id !== task.id)
    showToast('任务已删除', '任务已成功删除')
  } catch (e) {
    showToast('删除失败', '请稍后重试')
  }
}

async function deleteDayTask(task: any) {
  dayTaskMenuId.value = null
  const dk = formatDateKey(currentDate.value.getFullYear(), currentDate.value.getMonth(), currentDate.value.getDate())
  try {
    await taskStore.deleteTask(dk, task.id)
    if (tasks.value[dk]) {
      tasks.value[dk].tasks = tasks.value[dk].tasks.filter((t: any) => t.id !== task.id)
    }
    showToast('任务已删除', '任务已成功删除')
  } catch (e) {
    showToast('删除失败', '请稍后重试')
  }
}

function toggleTaskMenu(task: any, dateKey: string) {
  openMenuId.value = openMenuId.value === task.id ? null : task.id
}

function toggleDayTaskMenu(task: any) {
  dayTaskMenuId.value = dayTaskMenuId.value === task.id ? null : task.id
}

// 拖拽处理
function handleDragStart(e: DragEvent, task: any, sourceDateKey: string) {
  draggedTask.value = { task, sourceDateKey }
  if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move'
}

function handleDragOver(e: DragEvent, dateKey: string) {
  if (dateKey) dragOverDate.value = dateKey
}

function handleDragLeave() {
  dragOverDate.value = ''
}

function handleDrop(e: DragEvent, targetDateKey: string) {
  e.preventDefault()
  dragOverDate.value = ''
  if (!draggedTask.value || !targetDateKey || draggedTask.value.sourceDateKey === targetDateKey) {
    draggedTask.value = null
    return
  }

  const { task, sourceDateKey } = draggedTask.value
  const newTasks = { ...tasks.value }

  // 从源日期移除
  if (newTasks[sourceDateKey]) {
    newTasks[sourceDateKey] = { ...newTasks[sourceDateKey] }
    newTasks[sourceDateKey].tasks = newTasks[sourceDateKey].tasks.filter((t: any) => t.id !== task.id)
    if (newTasks[sourceDateKey].tasks.length === 0) {
      delete newTasks[sourceDateKey]
    }
  }

  // 添加到目标日期
  if (!newTasks[targetDateKey]) {
    newTasks[targetDateKey] = { targetAmount: 0, completedAmount: 0, tasks: [] }
  }
  newTasks[targetDateKey] = { ...newTasks[targetDateKey], tasks: [...newTasks[targetDateKey].tasks, task] }

  tasks.value = newTasks
  showToast('任务已移动', `${task.title || task.action} 已移动到 ${targetDateKey}`)
  draggedTask.value = null
}

// 公司名称
async function saveCompanyName() {
  editingCompany.value = false
  localStorage.setItem('company_name', companyName.value)
  showToast('保存成功', '公司名称已更新')
}

// 加载数据
async function loadTasks() {
  try {
    const res = await api.get('/tasks')
    if (res.data) {
      tasks.value = res.data
    }
  } catch (e) {
    // 从 localStorage 加载回退
    const saved = localStorage.getItem('calendar_tasks')
    if (saved) {
      try { tasks.value = JSON.parse(saved) } catch { tasks.value = {} }
    }
  }
}

// 关闭菜单（点击外部）
function handleGlobalClick() {
  openMenuId.value = null
  dayTaskMenuId.value = null
}

// 生命周期
onMounted(() => {
  const saved = localStorage.getItem('company_name')
  if (saved) companyName.value = saved

  document.addEventListener('click', handleGlobalClick)

  loadTasks()
})

onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick)
})
</script>
