/**
 * 小红书投流数据仓库 - 数据字典应用逻辑
 */

class DictionaryApp {
    constructor(data) {
        this.data = data;
        this.currentSection = 'fields';
        this.searchTerm = '';
        this.currentCategory = 'all';
        this.loadSize = 20;  // 每次加载数量
        this.displayedCount = {};  // 各分类已显示数量

        this.sections = [
            { id: 'fields', name: '字段标准', desc: '标准字段定义', icon: 'fa-table-columns', data: data.fields },
            { id: 'atomic', name: '原子指标', desc: '基础计算指标', icon: 'fa-atom', data: data.atomic },
            { id: 'composite', name: '复合指标', desc: '派生计算指标', icon: 'fa-calculator', data: data.composite },
            { id: 'codes', name: '标准代码', desc: '枚举值定义', icon: 'fa-list-ol', data: data.codes }
        ];
    }

    /**
     * 初始化应用
     */
    init() {
        // 初始化各分类已显示数量
        this.sections.forEach(s => {
            this.displayedCount[s.id] = this.loadSize;
        });

        this.renderTotalCount();
        this.renderSidebar();
        this.renderContent();
        this.bindEvents();
    }

    /**
     * 渲染总数量
     */
    renderTotalCount() {
        const totalEl = document.getElementById('total-count');
        if (!totalEl) return;

        const total = this.sections.reduce((sum, s) => sum + s.data.length, 0);
        totalEl.textContent = total;
    }

    /**
     * 渲染侧边栏
     */
    renderSidebar() {
        const nav = document.getElementById('sidebar-nav');
        if (!nav) return;

        nav.innerHTML = this.sections.map(section => `
            <div class="dict-nav-item ${section.id === this.currentSection ? 'active' : ''}"
                 data-section="${section.id}">
                <div class="dict-nav-icon ${section.id}">
                    <i class="fas ${section.icon}"></i>
                </div>
                <div class="dict-nav-text">
                    <div class="dict-nav-title">${section.name}</div>
                    <div class="dict-nav-desc">${section.desc}</div>
                </div>
                <span class="dict-nav-count">${section.data.length}</span>
            </div>
        `).join('');
    }

    /**
     * 渲染内容区域
     */
    renderContent() {
        const content = document.getElementById('main-content');
        if (!content) return;

        content.innerHTML = this.sections.map(section => {
            const categories = this.getCategories(section.id);
            return `
            <div id="${section.id}-content" class="dict-content ${section.id === this.currentSection ? 'active' : ''}">
                <div class="layer-header">
                    <div class="layer-title">
                        <span class="layer-badge" style="background: ${this.getSectionColor(section.id)}">${section.name}</span>
                        <h3>${section.desc}</h3>
                    </div>
                    <p class="layer-desc">${this.getSectionDescription(section.id)}</p>
                </div>

                <div class="category-tabs" data-section="${section.id}">
                    <span class="category-tab active" data-category="all">全部 <span class="tab-count">${section.data.length}</span></span>
                    ${categories.map(cat => `
                        <span class="category-tab" data-category="${cat.name}">${cat.shortName} <span class="tab-count">${cat.count}</span></span>
                    `).join('')}
                </div>

                <div class="search-bar">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="搜索字段名、中文名..." data-section="${section.id}">
                    <span class="search-count" data-count="${section.id}">${section.data.length} 条</span>
                </div>

                <div class="dict-table" data-table="${section.id}">
                    ${this.renderTable(section)}
                </div>

                <div class="load-more-area" data-loadmore="${section.id}">
                    ${this.renderLoadMore(section.id)}
                </div>
            </div>
        `}).join('');
    }

    /**
     * 获取分类列表
     */
    getCategories(sectionId) {
        const section = this.sections.find(s => s.id === sectionId);
        if (!section) return [];

        const categoryField = sectionId === 'codes' ? 'category' :
                              sectionId === 'fields' ? 'category' : 'process';

        const counts = {};
        section.data.forEach(item => {
            const cat = item[categoryField] || '未分类';
            counts[cat] = (counts[cat] || 0) + 1;
        });

        return Object.entries(counts).map(([name, count]) => ({
            name,
            shortName: this.getShortCategoryName(name),
            count
        })).sort((a, b) => b.count - a.count).slice(0, 8);
    }

    /**
     * 获取简短分类名（中文映射）
     */
    getShortCategoryName(name) {
        // 原子/复合指标的 process 字段中文映射
        const processNameMap = {
            'effect.sd': '种草直达',
            'effect.effect_default': '效果域_默认',
            'effect.ps': '产品种草',
            'effect.lg': '客资收集',
            'effect.ap': '应用推广',
            'effect.comp': '组件效果',
            'ad.fee': '消耗',
            'ad.plan': '规划',
            'ad.ad_default': '广告域_默认'
        };

        // 如果有完整路径映射，直接返回中文名
        if (processNameMap[name]) {
            return processNameMap[name];
        }

        // 字段标准和标准代码的分类提取最后一个层级
        const parts = name.split('.');
        return parts[parts.length - 1] || name;
    }

    /**
     * 获取分类颜色
     */
    getSectionColor(id) {
        const colors = {
            fields: '#2563EB',
            atomic: '#047857',
            composite: '#B45309',
            codes: '#6D28D9'
        };
        return colors[id] || '#666';
    }

    /**
     * 获取分类描述
     */
    getSectionDescription(id) {
        const descriptions = {
            fields: '定义数据仓库中使用的标准字段，包括字段英文名、中文名、数据类型等规范。',
            atomic: '定义基础度量指标，是构建复合指标的基础单元，包含计算函数和数据单位。',
            composite: '基于原子指标派生的复合计算指标，定义计算公式和业务逻辑。',
            codes: '定义业务枚举值和标准代码，确保数据一致性和规范性。'
        };
        return descriptions[id] || '';
    }

    /**
     * 渲染表格
     */
    renderTable(section) {
        const data = this.getFilteredData(section.id);
        const displayCount = this.displayedCount[section.id] || this.loadSize;
        const pageData = data.slice(0, displayCount);

        if (pageData.length === 0) {
            return `
                <div class="dict-empty">
                    <i class="fas fa-search"></i>
                    <p>未找到匹配的数据</p>
                </div>
            `;
        }

        switch (section.id) {
            case 'fields':
                return this.renderFieldsTable(pageData);
            case 'atomic':
                return this.renderAtomicTable(pageData);
            case 'composite':
                return this.renderCompositeTable(pageData);
            case 'codes':
                return this.renderCodesTable(pageData);
            default:
                return '';
        }
    }

    /**
     * 渲染字段标准表格
     */
    renderFieldsTable(data) {
        return `
            <table>
                <thead>
                    <tr>
                        <th>英文名</th>
                        <th>中文名</th>
                        <th>数据类型</th>
                        <th>业务定义</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(row => `
                        <tr>
                            <td><code class="field-name">${row.nameEn}</code></td>
                            <td>${row.nameCn}</td>
                            <td><span class="type-tag ${row.dataType}">${row.dataType}</span></td>
                            <td>${row.definition || '-'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    /**
     * 渲染原子指标表格
     */
    renderAtomicTable(data) {
        return `
            <table>
                <thead>
                    <tr>
                        <th>英文名</th>
                        <th>中文名</th>
                        <th>计算函数</th>
                        <th>数据单位</th>
                        <th>业务口径</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(row => `
                        <tr>
                            <td><code class="field-name">${row.nameEn}</code></td>
                            <td>${row.nameCn}</td>
                            <td>${row.function || '-'}</td>
                            <td>${row.unit || '-'}</td>
                            <td>${row.logic || '-'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    /**
     * 渲染复合指标表格
     */
    renderCompositeTable(data) {
        return `
            <table>
                <thead>
                    <tr>
                        <th>英文名</th>
                        <th>中文名</th>
                        <th>计算模式</th>
                        <th>计算公式</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(row => `
                        <tr>
                            <td><code class="field-name">${row.nameEn}</code></td>
                            <td>${row.nameCn}</td>
                            <td>${row.calcMode || '-'}</td>
                            <td>${row.formula ? `<code class="formula-code">${row.formula}</code>` : '-'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    /**
     * 渲染标准代码表格（支持展开枚举值）
     */
    renderCodesTable(data) {
        return `
            <div class="codes-list">
                ${data.map((row, idx) => `
                    <div class="code-item" data-code-idx="${idx}">
                        <div class="code-header">
                            <div class="code-info">
                                <code class="field-name">${row.code}</code>
                                <span class="code-cn">${row.nameCn}</span>
                                ${row.desc ? `<span class="code-desc">${row.desc}</span>` : ''}
                            </div>
                            <div class="code-meta">
                                <span class="code-count">${row.values ? row.values.length : 0} 个枚举值</span>
                                <i class="fas fa-chevron-down code-toggle"></i>
                            </div>
                        </div>
                        <div class="code-values">
                            ${row.values && row.values.length > 0 ? `
                                <table>
                                    <thead>
                                        <tr>
                                            <th>编码值</th>
                                            <th>中文名称</th>
                                            <th>英文名称</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${row.values.map(v => `
                                            <tr>
                                                <td><code>${v.value}</code></td>
                                                <td>${v.nameCn}</td>
                                                <td><code>${v.nameEn}</code></td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            ` : '<p class="no-values">暂无枚举值</p>'}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    /**
     * 获取过滤后的数据
     */
    getFilteredData(sectionId) {
        const section = this.sections.find(s => s.id === sectionId);
        if (!section) return [];

        let data = section.data;

        // 按分类过滤
        if (this.currentCategory && this.currentCategory !== 'all') {
            const categoryField = sectionId === 'codes' ? 'category' :
                                  sectionId === 'fields' ? 'category' : 'process';
            data = data.filter(item => {
                const cat = item[categoryField] || '未分类';
                return cat === this.currentCategory;
            });
        }

        // 按搜索词过滤
        if (this.searchTerm) {
            const term = this.searchTerm.toLowerCase();
            data = data.filter(item => {
                const searchFields = [
                    item.nameEn,
                    item.nameCn,
                    item.category,
                    item.process,
                    item.code
                ].filter(Boolean);

                return searchFields.some(field =>
                    field.toLowerCase().includes(term)
                );
            });
        }

        return data;
    }

    /**
     * 渲染加载更多
     */
    renderLoadMore(sectionId) {
        const data = this.getFilteredData(sectionId);
        const displayCount = this.displayedCount[sectionId] || this.loadSize;
        const remaining = data.length - displayCount;

        if (remaining <= 0) {
            if (data.length > this.loadSize) {
                return `<div class="load-complete">已加载全部 ${data.length} 条数据</div>`;
            }
            return '';
        }

        return `
            <div class="load-more-trigger" data-section="${sectionId}">
                <div class="load-more-btn">
                    <i class="fas fa-angle-down"></i>
                    <span>下拉加载更多</span>
                    <span class="load-more-count">还有 ${remaining} 条</span>
                </div>
            </div>
        `;
    }

    /**
     * 绑定事件
     */
    bindEvents() {
        // 侧边栏导航点击
        const nav = document.getElementById('sidebar-nav');
        if (nav) {
            nav.addEventListener('click', (e) => {
                const item = e.target.closest('.dict-nav-item');
                if (!item) return;

                const sectionId = item.dataset.section;
                this.switchSection(sectionId);
            });
        }

        // 搜索框输入
        const content = document.getElementById('main-content');
        if (content) {
            content.addEventListener('input', (e) => {
                if (e.target.matches('.search-bar input')) {
                    this.searchTerm = e.target.value;
                    // 重置显示数量
                    this.displayedCount[e.target.dataset.section] = this.loadSize;
                    this.updateTable(e.target.dataset.section);
                }
            });

            // 枚举值展开/收起
            content.addEventListener('click', (e) => {
                const codeHeader = e.target.closest('.code-header');
                if (codeHeader) {
                    const codeItem = codeHeader.closest('.code-item');
                    codeItem.classList.toggle('expanded');
                    return;
                }
            });

            // 分类标签点击
            content.addEventListener('click', (e) => {
                const tab = e.target.closest('.category-tab');
                if (tab) {
                    const tabsContainer = tab.closest('.category-tabs');
                    const sectionId = tabsContainer.dataset.section;
                    const category = tab.dataset.category;

                    // 更新激活状态
                    tabsContainer.querySelectorAll('.category-tab').forEach(t => {
                        t.classList.toggle('active', t === tab);
                    });

                    // 更新当前分类并刷新表格，重置显示数量
                    this.currentCategory = category;
                    this.displayedCount[sectionId] = this.loadSize;
                    this.updateTable(sectionId);
                    return;
                }
            });

            // 滚动加载更多
            content.addEventListener('scroll', () => {
                this.handleScroll(content);
            });
        }
    }

    /**
     * 处理滚动加载更多
     */
    handleScroll(container) {
        const sectionId = this.currentSection;
        const data = this.getFilteredData(sectionId);
        const displayCount = this.displayedCount[sectionId] || this.loadSize;

        // 如果已全部加载，不处理
        if (displayCount >= data.length) return;

        // 检测是否滚动到底部附近
        const scrollBottom = container.scrollHeight - container.scrollTop - container.clientHeight;
        if (scrollBottom < 100) {
            this.loadMore(sectionId);
        }
    }

    /**
     * 加载更多数据
     */
    loadMore(sectionId) {
        const data = this.getFilteredData(sectionId);
        const currentCount = this.displayedCount[sectionId] || this.loadSize;

        // 增加显示数量
        this.displayedCount[sectionId] = Math.min(currentCount + this.loadSize, data.length);

        // 更新表格
        this.updateTable(sectionId);
    }

    /**
     * 切换分类
     */
    switchSection(sectionId) {
        this.currentSection = sectionId;
        this.searchTerm = '';
        this.currentCategory = 'all';
        this.displayedCount[sectionId] = this.loadSize;

        // 更新导航状态
        document.querySelectorAll('.dict-nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.section === sectionId);
        });

        // 更新内容显示
        document.querySelectorAll('.dict-content').forEach(content => {
            content.classList.toggle('active', content.id === `${sectionId}-content`);
        });

        // 清空搜索框
        const input = document.querySelector(`input[data-section="${sectionId}"]`);
        if (input) input.value = '';
    }

    /**
     * 更新表格
     */
    updateTable(sectionId) {
        const section = this.sections.find(s => s.id === sectionId);
        if (!section) return;

        const filteredData = this.getFilteredData(sectionId);

        // 更新搜索计数
        const countEl = document.querySelector(`[data-count="${sectionId}"]`);
        if (countEl) {
            countEl.textContent = `${filteredData.length} 条`;
        }

        // 更新表格
        const tableEl = document.querySelector(`[data-table="${sectionId}"]`);
        if (tableEl) {
            tableEl.innerHTML = this.renderTable(section);
        }

        // 更新加载更多
        const loadMoreEl = document.querySelector(`[data-loadmore="${sectionId}"]`);
        if (loadMoreEl) {
            loadMoreEl.innerHTML = this.renderLoadMore(sectionId);
        }
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    const app = new DictionaryApp(DATA_DICTIONARY);
    app.init();
});
