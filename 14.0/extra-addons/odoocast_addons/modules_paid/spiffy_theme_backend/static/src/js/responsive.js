odoo.define("spiffy_theme_backend.responsive", function (require) {
    const config = require("web.config");
    const ControlPanel = require("web.ControlPanel");
    const SearchPanel = require("web/static/src/js/views/search_panel.js");
    const {QWeb, Context} = owl;
    const {useState, useContext} = owl.hooks;

    const deviceContext = new Context({
        isMobile: config.device.isMobile,
        size_class: config.device.size_class,
        SIZES: config.device.SIZES,
    });

    ControlPanel.patch("spiffy_theme_backend.ControlPanelMobile", (T) => {
        class ControlPanelPatchResponsive extends T {
            constructor() {
                super(...arguments);
                this.state = useState({
                    mobileSearchMode: "",
                });
                this.device = useContext(deviceContext);
            }
        }
        return ControlPanelPatchResponsive;
    });

    // Patch search panel to add functionality for mobile view
    SearchPanel.patch("spiffy_theme_backend.SearchPanelMobile", (T) => {
        class SearchPanelPatchResponsive extends T {
            constructor() {
                super(...arguments);
                this.state.mobileSearch = false;
                this.device = useContext(deviceContext);
            }
            getActiveSummary() {
                const selection = [];
                for (const filter of this.model.get("sections")) {
                    let filterValues = [];
                    if (filter.type === "category") {
                        if (filter.activeValueId) {
                            const parentIds = this._getAncestorValueIds(
                                filter,
                                filter.activeValueId
                            );
                            filterValues = [...parentIds, filter.activeValueId].map(
                                (valueId) => filter.values.get(valueId).display_name
                            );
                        }
                    } else {
                        let values = [];
                        if (filter.groups) {
                            values = Array.from(
                                filter.groups.values(),
                                (g) => g.values
                            ).flat();
                        }
                        if (filter.values) {
                            values = [...filter.values.values()];
                        }
                        filterValues = values
                            .filter((v) => v.checked)
                            .map((v) => v.display_name);
                    }
                    if (filterValues.length) {
                        selection.push({
                            values: filterValues,
                            icon: filter.icon,
                            color: filter.color,
                            type: filter.type,
                        });
                    }
                }
                return selection;
            }
        }
        return SearchPanelPatchResponsive;
    });

    return {
        deviceContext: deviceContext,
    };
});