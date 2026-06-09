<template>
  <AppLayout current-page="settings" title="系统设置" subtitle="系统配置与管理">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <div class="flex gap-2 mb-6">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="['px-4 py-2 rounded-xl text-sm transition-all', activeTab === tab.key ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50']">{{ tab.label }}</button>
      </div>

      <!-- 系统信息 -->
      <div v-if="activeTab === 'system'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 max-w-2xl">
        <h2 class="font-bold text-slate-800 mb-4">系统信息</h2>
        <div class="space-y-4">
          <div><label class="text-sm text-slate-500 block mb-1">系统名称</label><input v-model="config.systemName" class="w-full h-10 px-4 rounded-xl border border-slate-200 text-sm outline-none" /></div>
          <div><label class="text-sm text-slate-500 block mb-1">公司名称</label><input v-model="config.companyName" class="w-full h-10 px-4 rounded-xl border border-slate-200 text-sm outline-none" /></div>
          <div><label class="text-sm text-slate-500 block mb-1">日目标营业额（元）</label><input v-model="config.dailyTarget" type="number" class="w-full h-10 px-4 rounded-xl border border-slate-200 text-sm outline-none" /></div>
          <button @click="saveConfig" class="px-5 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">💾 保存配置</button>
        </div>
      </div>

      <!-- 账号管理 -->
      <div v-if="activeTab === 'accounts'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 max-w-4xl">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-bold text-slate-800">账号管理</h2>
          <button @click="showAccountForm = true" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm">+ 添加账号</button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full"><thead><tr class="border-b border-slate-100"><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">账号</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">姓名</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">角色</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">公司</th><th class="px-4 py-3 text-center text-sm font-semibold text-slate-600">状态</th><th class="px-4 py-3 text-center text-sm font-semibold text-slate-600">操作</th></tr></thead>
            <tbody>
              <tr v-for="a in accounts" :key="a.id" class="border-b border-slate-50"><td class="px-4 py-3 text-sm font-medium">{{ a.account }}</td><td class="px-4 py-3 text-sm">{{ a.name }}</td><td class="px-4 py-3 text-sm"><span :class="['px-2 py-0.5 rounded text-xs', a.role === '管理员' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-600']">{{ a.role }}</span></td><td class="px-4 py-3 text-sm">{{ a.company }}</td><td class="px-4 py-3 text-center"><span :class="['px-2 py-0.5 rounded text-xs', a.status === 'active' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700']">{{ a.status === 'active' ? '正常' : '禁用' }}</span></td><td class="px-4 py-3 text-center"><button @click="editAccount(a)" class="text-blue-600 text-sm mr-2">✎</button><button @click="deleteAccount(a.id)" class="text-red-500 text-sm">🗑</button></td></tr>
            </tbody></table>
        </div>
      </div>

      <!-- 数据管理 -->
      <div v-if="activeTab === 'data'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 max-w-2xl">
        <h2 class="font-bold text-slate-800 mb-4">数据管理</h2>
        <div class="space-y-4">
          <div class="p-4 bg-slate-50 rounded-xl">
            <h3 class="font-medium text-slate-800 mb-2">数据操作</h3>
            <div class="flex flex-wrap gap-3">
              <button @click="exportData" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700">📥 导出数据 (JSON)</button>
              <button @click="clearAllData" class="px-4 py-2 bg-red-600 text-white rounded-xl text-sm hover:bg-red-700">🗑 清除所有数据</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 账号弹窗 -->
      <Teleport to="body">
        <div v-if="showAccountForm" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showAccountForm = false">
          <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
            <h3 class="font-bold text-slate-800 text-lg mb-4">{{ editingAccountId ? '编辑账号' : '添加账号' }}</h3>
            <div class="space-y-3">
              <select v-model="accountForm.role" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none"><option value="管理员">管理员</option><option value="用户">用户</option></select>
              <input v-model="accountForm.name" placeholder="姓名" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
              <input v-model="accountForm.account" placeholder="账号" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
              <input v-model="accountForm.password" type="password" placeholder="密码" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
              <input v-model="accountForm.company" placeholder="所属公司" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            </div>
            <div class="flex gap-3 mt-6"><button @click="showAccountForm = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button><button @click="saveAccount" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm">保存</button></div>
          </div>
        </div>
      </Teleport>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'

const activeTab = ref('system')
const tabs = [
  { key: 'system', label: '系统信息' },
  { key: 'accounts', label: '账号管理' },
  { key: 'data', label: '数据管理' }
]

const config = ref({ systemName: 'X10增长引擎', companyName: '涌动花鱼科技有限公司', dailyTarget: '500000' })
const accounts = ref<any[]>([])
const showAccountForm = ref(false)
const editingAccountId = ref<string | null>(null)
const accountForm = ref({ role: '用户', name: '', account: '', password: '', company: '' })

function saveConfig() {
  localStorage.setItem('system_config', JSON.stringify(config.value))
  localStorage.setItem('company_name', config.value.companyName)
  alert('配置已保存')
}

function editAccount(a: any) { accountForm.value = { ...a }; editingAccountId.value = a.id; showAccountForm.value = true }

function saveAccount() {
  if (!accountForm.value.name || !accountForm.value.account || !accountForm.value.password) { alert('请填写完整信息'); return }
  if (editingAccountId.value) {
    const i = accounts.value.findIndex(a => a.id === editingAccountId.value)
    if (i >= 0) accounts.value[i] = { ...accountForm.value, id: editingAccountId.value, status: 'active' }
  } else {
    accounts.value.push({ ...accountForm.value, id: Date.now().toString(), status: 'active' })
  }
  saveAccounts(); showAccountForm.value = false; editingAccountId.value = null
  accountForm.value = { role: '用户', name: '', account: '', password: '', company: '' }
}

function deleteAccount(id: string) { if (!confirm('确定删除？')) return; accounts.value = accounts.value.filter(a => a.id !== id); saveAccounts() }
function saveAccounts() { localStorage.setItem('accounts_list', JSON.stringify(accounts.value)) }

function exportData() {
  const data: any = {}
  const keys = ['calendar_tasks', 'work_reports', 'influencer_records', 'daren_resources', 'consensus_archives', 'training_problems', 'accounts_list', 'system_config', 'company_name']
  keys.forEach(k => { const v = localStorage.getItem(k); if (v) data[k] = JSON.parse(v) })
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = `x10_backup_${new Date().toISOString().split('T')[0]}.json`; a.click()
  URL.revokeObjectURL(url)
}

function clearAllData() {
  if (!confirm('⚠️ 此操作将清除所有本地数据，不可恢复！确定继续？')) return
  if (!confirm('再次确认：清除所有数据？')) return
  const keys = ['calendar_tasks', 'work_reports', 'influencer_records', 'daren_resources', 'consensus_archives', 'training_problems']
  keys.forEach(k => localStorage.removeItem(k))
  alert('数据已清除')
}

onMounted(() => {
  const saved = localStorage.getItem('system_config')
  if (saved) { try { config.value = JSON.parse(saved) } catch {} }
  const acc = localStorage.getItem('accounts_list')
  if (acc) { try { accounts.value = JSON.parse(acc) } catch {} }
})
</script>
