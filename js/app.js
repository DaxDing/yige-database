/**
 * 小红书投流数据仓库 - 应用逻辑
 */

class DataWarehouseApp {
    constructor(data) {
        this.data = data;
        this.currentLayer = 'ods';
    }

    /**
     * 初始化应用
     */
    init() {
        this.renderVersion();
        this.renderTotalCount();
        this.renderSidebar();
        this.renderContent();
        this.bindEvents();
    }

    /**
     * 渲染总表数量
     */
    renderTotalCount() {
        const totalEl = document.getElementById('total-count');
        if (!totalEl) return;

        const total = this.data.layers.reduce((sum, layer) => sum + this.getTableCount(layer), 0);
        totalEl.textContent = total;
    }

    /**
     * 渲染版本信息
     */
    renderVersion() {
        const versionEl = document.getElementById('version');
        const dateEl = document.getElementById('update-date');
        if (versionEl) versionEl.textContent = `设计版本 v${this.data.version}`;
        if (dateEl) dateEl.textContent = this.data.updateDate;
    }

    /**
     * 渲染侧边栏导航
     */
    renderSidebar() {
        const nav = document.getElementById('sidebar-nav');
        if (!nav) return;

        nav.innerHTML = this.data.layers.map(layer => `
            <div class="nav-item ${layer.id === this.currentLayer ? 'active' : ''}"
                 data-layer="${layer.id}">
                <span class="nav-dot ${layer.id}"></span>
                <div class="nav-text">
                    <div class="nav-title">${layer.name}</div>
                    <div class="nav-desc">${layer.fullName}</div>
                </div>
                <span class="nav-count">${this.getTableCount(layer)}</span>
            </div>
        `).join('');
    }

    /**
     * 获取层级表数量（支持分组和子分组）
     */
    getTableCount(layer) {
        if (layer.groups && layer.groups.length > 0) {
            return layer.groups.reduce((sum, group) => {
                // 如果有子分组，递归计算
                if (group.subgroups && group.subgroups.length > 0) {
                    return sum + group.subgroups.reduce((subSum, subgroup) => subSum + subgroup.tables.length, 0);
                }
                return sum + group.tables.length;
            }, 0);
        }
        return layer.tables.length;
    }

    /**
     * 获取分组表数量（包含子分组）
     */
    getGroupTableCount(group) {
        if (group.subgroups && group.subgroups.length > 0) {
            return group.subgroups.reduce((sum, subgroup) => sum + subgroup.tables.length, 0);
        }
        return group.tables.length;
    }

    /**
     * 渲染内容区域
     */
    renderContent() {
        const content = document.getElementById('main-content');
        if (!content) return;

        content.innerHTML = this.data.layers.map(layer => `
            <div id="${layer.id}-content" class="layer-content ${layer.id === this.currentLayer ? 'active' : ''}">
                <div class="layer-header">
                    <div class="layer-title">
                        <span class="layer-badge ${layer.id}">${layer.name}</span>
                        <h3>${layer.fullName}</h3>
                    </div>
                    <p class="layer-desc">${layer.description}</p>
                </div>
                ${this.renderTables(layer)}
            </div>
        `).join('');
    }

    /**
     * 渲染表列表（支持分组）
     */
    renderTables(layer) {
        // 有分组的情况
        if (layer.groups && layer.groups.length > 0) {
            return this.renderGroupedTables(layer);
        }

        // 无表的情况
        if (layer.tables.length === 0) {
            return `
                <div class="empty-state">
                    <div class="empty-icon">
                        <i class="fas fa-hourglass-half"></i>
                    </div>
                    <h4>待规划</h4>
                    <p>${layer.name} 层表结构将根据具体业务需求进行设计</p>
                </div>
            `;
        }

        // 普通表列表
        return this.renderTableList(layer.tables, layer.id);
    }

    /**
     * 渲染分组表
     */
    renderGroupedTables(layer) {
        return `
            <div class="group-tabs">
                ${layer.groups.map((group, index) => `
                    <span class="group-tab ${index === 0 ? 'active' : ''}"
                          data-group="${index}">${group.name}
                          <span class="group-count">${this.getGroupTableCount(group)}</span>
                    </span>
                `).join('')}
            </div>
            ${layer.groups.map((group, index) => `
                <div class="group-content ${index === 0 ? 'active' : ''}" data-group="${index}">
                    ${this.renderGroupContent(group, layer.id)}
                </div>
            `).join('')}
        `;
    }

    /**
     * 渲染分组内容（支持子分组）
     */
    renderGroupContent(group, layerId) {
        // 有子分组的情况
        if (group.subgroups && group.subgroups.length > 0) {
            return `
                <div class="subgroup-tabs">
                    ${group.subgroups.map((subgroup, index) => `
                        <span class="subgroup-tab ${index === 0 ? 'active' : ''}"
                              data-subgroup="${index}">${subgroup.name}
                              <span class="subgroup-count">${subgroup.tables.length}</span>
                        </span>
                    `).join('')}
                </div>
                ${group.subgroups.map((subgroup, index) => `
                    <div class="subgroup-content ${index === 0 ? 'active' : ''}" data-subgroup="${index}">
                        ${subgroup.tables.length > 0
                            ? this.renderTableList(subgroup.tables, layerId, group.name)
                            : this.renderGroupEmpty(subgroup.name)
                        }
                    </div>
                `).join('')}
            `;
        }

        // 无子分组
        if (group.tables.length > 0) {
            return this.renderTableList(group.tables, layerId, group.name);
        }
        return this.renderGroupEmpty(group.name);
    }

    /**
     * 渲染空分组状态
     */
    renderGroupEmpty(groupName) {
        return `
            <div class="empty-state small">
                <div class="empty-icon">
                    <i class="fas fa-plus-circle"></i>
                </div>
                <h4>待添加</h4>
                <p>${groupName}相关表结构将根据业务需求设计</p>
            </div>
        `;
    }

    /**
     * 渲染表列表
     */
    renderTableList(tables, layerId, groupName = '') {
        // 所有层都支持展开
        return tables.map(table => {
            const fieldCount = this.getFieldCount(layerId, groupName, table.name);
            return `
            <div class="table-card expandable">
                <div class="table-header ${layerId}" data-expandable="true">
                    <div class="table-info">
                        <span class="table-name">${table.name}</span>
                        <span class="table-desc">${table.desc}</span>
                    </div>
                    <div class="table-meta">
                        ${table.tags.map(tag => `<span class="table-tag">${tag}</span>`).join('')}
                        <span class="field-count">${fieldCount} 字段</span>
                        <i class="fas fa-chevron-down table-toggle"></i>
                    </div>
                </div>
                ${this.renderLayerFields(layerId, groupName, table.name)}
            </div>
        `}).join('');
    }

    /**
     * 获取表字段数量
     */
    getFieldCount(layerId, groupName = '', tableName = '') {
        let fields = [];
        switch (layerId) {
            case 'ods':
                fields = this.getOdsFields(groupName, tableName);
                break;
            case 'dwd':
                fields = this.getDwdFields(groupName, tableName);
                break;
            case 'dim':
                fields = this.getDimFields(tableName);
                break;
            case 'bridge':
                fields = this.getBridgeFields(tableName);
                break;
            case 'dws':
                fields = this.getDwsFields(tableName);
                break;
            case 'ads':
                fields = this.getAdsFields();
                break;
            default:
                fields = [...(this.data.commonTailFields || [])];
        }
        return fields.length;
    }

    /**
     * 根据层级渲染字段
     */
    renderLayerFields(layerId, groupName = '', tableName = '') {
        let fields = [];

        switch (layerId) {
            case 'ods':
                fields = this.getOdsFields(groupName, tableName);
                break;
            case 'dwd':
                fields = this.getDwdFields(groupName, tableName);
                break;
            case 'dim':
                fields = this.getDimFields(tableName);
                break;
            case 'bridge':
                fields = this.getBridgeFields(tableName);
                break;
            case 'dws':
                fields = this.getDwsFields(tableName);
                break;
            case 'ads':
                fields = this.getAdsFields();
                break;
            default:
                fields = [...(this.data.commonTailFields || [])];
        }

        return this.renderFieldsTable(fields);
    }

    /**
     * 获取表字段（统一入口，优先从 TABLE_DEFINITIONS 获取）
     */
    getTableFieldsFromDefinitions(tableName) {
        if (typeof TABLE_DEFINITIONS !== 'undefined' && TABLE_DEFINITIONS[tableName]) {
            return TABLE_DEFINITIONS[tableName].fields;
        }
        return null;
    }

    /**
     * 获取 ODS 层字段
     */
    getOdsFields(groupName = '', tableName = '') {
        // 优先从统一表定义获取
        const definedFields = this.getTableFieldsFromDefinitions(tableName);
        if (definedFields) return definedFields;

        // 兼容旧的表级字段定义
        const tableFields = this.data.odsTableFields || {};
        if (tableName && tableFields[tableName]) {
            return tableFields[tableName];
        }

        // 使用通用字段 + 分组字段
        let fields = [...(this.data.odsFields || [])];
        const groupFields = this.data.odsGroupFields || {};
        if (groupName && groupFields[groupName]) {
            const insertIndex = fields.findIndex(f => f.name === 'dt');
            fields.splice(insertIndex, 0, ...groupFields[groupName]);
        }
        return fields;
    }

    /**
     * 获取 DWD 层字段
     */
    getDwdFields(groupName = '', tableName = '') {
        // 优先从统一表定义获取
        const definedFields = this.getTableFieldsFromDefinitions(tableName);
        if (definedFields) return definedFields;

        // 兼容旧的表级字段定义
        const tableFields = this.data.dwdTableFields || {};
        if (tableName && tableFields[tableName]) {
            return tableFields[tableName];
        }

        // 默认通用字段
        return [
            { name: 'dt', nameCn: '数据时间段', type: 'STRING', desc: '数据统计的时间段范围', example: '2026-01-06 14:00 - 14:59' },
            { name: '...', nameCn: '业务字段', type: '-', desc: '根据具体表定义的业务明细字段', example: '-' },
            ...(this.data.commonTailFields || [])
        ];
    }

    /**
     * 获取 DIM 层字段
     */
    getDimFields(tableName = '') {
        // 优先从统一表定义获取
        const definedFields = this.getTableFieldsFromDefinitions(tableName);
        if (definedFields) return definedFields;

        // 从 dimTableFields 获取
        const dimTableFields = this.data.dimTableFields || {};
        if (tableName && dimTableFields[tableName]) {
            return dimTableFields[tableName];
        }

        // 从表名中提取维度名称
        const dimMatch = tableName.match(/dim_xhs_(\w+)_df/);
        const dimName = dimMatch ? dimMatch[1] : 'dimension';

        return [
            { name: `${dimName}_id`, nameCn: '维度主键', type: 'STRING', desc: '维度表主键，唯一标识', example: '-', key: 'PK' },
            { name: '...', nameCn: '维度属性', type: '-', desc: '根据具体维度定义的属性字段', example: '-' },
            ...(this.data.commonTailFields || [])
        ];
    }

    /**
     * 获取桥接表字段
     */
    getBridgeFields(tableName = '') {
        // 从 bridgeTableFields 获取
        const bridgeTableFields = this.data.bridgeTableFields || {};
        if (tableName && bridgeTableFields[tableName]) {
            return bridgeTableFields[tableName];
        }

        return [
            { name: 'note_id', nameCn: '笔记ID', type: 'STRING', desc: '笔记唯一标识', example: '6823119876543210' },
            { name: 'project_id', nameCn: '项目ID', type: 'STRING', desc: '项目唯一标识', example: 'PJ20260001' },
            { name: 'relation_type', nameCn: '关联类型', type: 'STRING', desc: '笔记与项目的关联类型', example: 'primary' },
            ...(this.data.commonTailFields || [])
        ];
    }

    /**
     * 获取 DWS 层字段
     */
    getDwsFields(tableName = '') {
        // 从 dwsTableFields 获取
        const dwsTableFields = this.data.dwsTableFields || {};
        if (tableName && dwsTableFields[tableName]) {
            return dwsTableFields[tableName];
        }

        return [
            { name: 'stat_date', nameCn: '统计日期', type: 'STRING', desc: '汇总统计日期', example: '2026-01-06' },
            { name: '...', nameCn: '汇总指标', type: '-', desc: '根据具体表定义的聚合指标字段', example: '-' },
            ...(this.data.commonTailFields || [])
        ];
    }

    /**
     * 获取 ADS 层字段
     */
    getAdsFields() {
        return [
            { name: 'report_date', nameCn: '报表日期', type: 'STRING', desc: '报表数据日期', example: '2026-01-06' },
            { name: '...', nameCn: '应用指标', type: '-', desc: '根据具体业务场景定义的应用指标', example: '-' },
            ...(this.data.commonTailFields || [])
        ];
    }

    /**
     * 渲染字段表格
     */
    renderFieldsTable(fields) {
        // 检查是否有序号字段和分类字段
        const hasSeq = fields.some(f => f.seq !== undefined);
        const hasCat = fields.some(f => f.cat !== undefined);
        const colCount = (hasSeq ? 1 : 0) + 5; // 计算列数

        // 按分类分组字段
        let groupedFields = [];
        if (hasCat) {
            let currentCat = null;
            fields.forEach(field => {
                if (field.cat !== currentCat) {
                    currentCat = field.cat;
                    groupedFields.push({ isCatHeader: true, cat: currentCat, count: fields.filter(f => f.cat === currentCat).length });
                }
                groupedFields.push(field);
            });
        } else {
            groupedFields = fields;
        }

        return `
            <div class="table-fields">
                <table class="fields-table ${hasCat ? 'has-categories' : ''}">
                    <thead>
                        <tr>
                            ${hasSeq ? '<th class="seq-col">序号</th>' : ''}
                            <th>字段名</th>
                            <th>中文名</th>
                            <th>类型</th>
                            <th>说明</th>
                            <th>示例</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${groupedFields.map(item => {
                            if (item.isCatHeader) {
                                return `<tr class="category-row">
                                    <td colspan="${colCount}">
                                        <span class="category-name">${item.cat}</span>
                                        <span class="category-count">${item.count}</span>
                                    </td>
                                </tr>`;
                            }
                            const isJson = item.type === 'JSON';
                            return `<tr>
                                ${hasSeq ? `<td class="seq-col">${item.seq || '-'}</td>` : ''}
                                <td>
                                    <code>${item.name}</code>
                                    ${item.key ? `<span class="field-key ${item.key.toLowerCase()}">${item.key}</span>` : ''}
                                </td>
                                <td>${item.nameCn}</td>
                                <td>${isJson
                                    ? `<span class="type-badge json clickable" data-schema="${item.name}" title="点击查看详情"><i class="fas fa-external-link-alt"></i> JSON</span>`
                                    : `<span class="type-badge ${item.type}">${item.type}</span>`
                                }</td>
                                <td>${item.desc}</td>
                                <td><code class="example-value">${item.example || '-'}</code></td>
                            </tr>`;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    /**
     * 绑定事件
     */
    bindEvents() {
        const nav = document.getElementById('sidebar-nav');
        if (!nav) return;

        // 侧边栏层级切换
        nav.addEventListener('click', (e) => {
            const navItem = e.target.closest('.nav-item');
            if (!navItem) return;

            const layerId = navItem.dataset.layer;
            this.switchLayer(layerId);
        });

        // 层内分组标签切换
        const content = document.getElementById('main-content');
        if (!content) return;

        content.addEventListener('click', (e) => {
            // 处理一级分组标签
            const groupTab = e.target.closest('.group-tab');
            if (groupTab) {
                const groupIndex = groupTab.dataset.group;
                const layerContent = groupTab.closest('.layer-content');

                // 更新标签状态
                layerContent.querySelectorAll('.group-tab').forEach(tab => {
                    tab.classList.toggle('active', tab.dataset.group === groupIndex);
                });

                // 更新内容显示
                layerContent.querySelectorAll('.group-content').forEach(content => {
                    content.classList.toggle('active', content.dataset.group === groupIndex);
                });
                return;
            }

            // 处理二级分组标签
            const subgroupTab = e.target.closest('.subgroup-tab');
            if (subgroupTab) {
                const subgroupIndex = subgroupTab.dataset.subgroup;
                const groupContent = subgroupTab.closest('.group-content');

                // 更新标签状态
                groupContent.querySelectorAll('.subgroup-tab').forEach(tab => {
                    tab.classList.toggle('active', tab.dataset.subgroup === subgroupIndex);
                });

                // 更新内容显示
                groupContent.querySelectorAll('.subgroup-content').forEach(content => {
                    content.classList.toggle('active', content.dataset.subgroup === subgroupIndex);
                });
                return;
            }

            // 处理 ODS 表展开/收起
            const tableHeader = e.target.closest('.table-header[data-expandable]');
            if (tableHeader) {
                const tableCard = tableHeader.closest('.table-card');
                tableCard.classList.toggle('expanded');
            }

            // 处理 JSON 字段点击弹框
            const jsonBadge = e.target.closest('.type-badge.json.clickable');
            if (jsonBadge) {
                const schemaName = jsonBadge.dataset.schema;
                this.showJsonSchemaModal(schemaName);
            }
        });

        // 关闭弹框事件
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('json-modal-overlay') || e.target.classList.contains('json-modal-close')) {
                this.closeJsonSchemaModal();
            }
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeJsonSchemaModal();
        });
    }

    /**
     * 显示 JSON Schema 弹框
     */
    showJsonSchemaModal(schemaName) {
        // 从 TABLE_DEFINITIONS 获取 schema
        const table = TABLE_DEFINITIONS['dwd_xhs_creative_hourly_di'];
        if (!table || !table.metricsSchema || !table.metricsSchema[schemaName]) return;

        const schema = table.metricsSchema[schemaName];
        const modal = document.createElement('div');
        modal.className = 'json-modal-overlay';
        modal.innerHTML = `
            <div class="json-modal">
                <div class="json-modal-header">
                    <h3>${schema.nameCn}</h3>
                    <span class="json-modal-close"><i class="fas fa-times"></i></span>
                </div>
                <div class="json-modal-body">
                    <table class="json-schema-table">
                        <thead>
                            <tr>
                                <th>字段名</th>
                                <th>中文名</th>
                                <th>类型</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${schema.fields.map(f => `
                                <tr>
                                    <td><code>${f.name}</code></td>
                                    <td>${f.nameCn}</td>
                                    <td><span class="type-badge ${f.type}">${f.type}</span></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        requestAnimationFrame(() => modal.classList.add('active'));
    }

    /**
     * 关闭 JSON Schema 弹框
     */
    closeJsonSchemaModal() {
        const modal = document.querySelector('.json-modal-overlay');
        if (modal) {
            modal.classList.remove('active');
            setTimeout(() => modal.remove(), 200);
            document.body.style.overflow = '';
        }
    }

    /**
     * 切换层级
     */
    switchLayer(layerId) {
        this.currentLayer = layerId;

        // 更新导航状态
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.layer === layerId);
        });

        // 更新内容显示
        document.querySelectorAll('.layer-content').forEach(content => {
            content.classList.toggle('active', content.id === `${layerId}-content`);
        });
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    const app = new DataWarehouseApp(DATA_WAREHOUSE);
    app.init();
});
