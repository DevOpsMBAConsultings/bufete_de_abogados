/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class LawDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            stats: {
                advice: { total: 0, new: 0, closed: 0 },
                cases: { total: 0, won: 0 },
                hearings: { total: 0, new: 0, open: 0, closed: 0 },
                invoices: { total: 0, paid: 0, due: 0 }
            },
            lawyers: [],
            selectedLawyer: null,
        });

        onWillStart(async () => {
            await this.loadData();
            this.state.lawyers = await this.orm.searchRead("lawyer", [], ["id", "name"]);
        });
    }

    async loadData() {
        const stats = await this.orm.call("lawyer.case", "get_dashboard_stats", [], {
            lawyer_id: this.state.selectedLawyer,
        });
        this.state.stats = stats;
    }

    async onLawyerChange(ev) {
        this.state.selectedLawyer = ev.target.value ? parseInt(ev.target.value) : null;
        await this.loadData();
    }
}

LawDashboard.template = "bufete_de_abogados.LawDashboard";

registry.category("actions").add("lawyer_dashboard_main", LawDashboard);
