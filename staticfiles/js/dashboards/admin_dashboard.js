async function loadDashboard() {
    try {
        const res = await fetch('/finances/dashboard/summary/');
        if (!res.ok){
            const message = await res.json()
            toast.show(message.error, 'error')
            throw new Error('Failed to fetch dashboard data');
        };
        const data = await res.json();

        document.getElementById('stat-students').textContent = data.stats.total_students;
        document.getElementById('stat-teachers').textContent = data.stats.total_teachers;
        document.getElementById('stat-classes').textContent = data.stats.total_classes;
        document.getElementById('stat-fees').textContent = 'GHS ' + parseFloat(data.stats.fees_collected).toLocaleString();
        document.getElementById('stat-fees-percent').textContent = data.fee_status.collection_percentage + '% of target';

        document.getElementById('fee-term-label').textContent = `Term ${data.current_term} · Academic Year ${data.academic_year}`;

        document.getElementById('fee-collected').textContent = 'GHS ' + parseFloat(data.fee_status.collected).toLocaleString();
        document.getElementById('fee-percent').textContent = `(${data.fee_status.collection_percentage}%)`;
        document.getElementById('fee-progress-bar').style.width = data.fee_status.collection_percentage + '%';

        document.getElementById('fee-partial-amount').textContent = 'GHS ' + parseFloat(data.fee_status.partially_paid_amount).toLocaleString();
        document.getElementById('fee-partial-count').textContent = data.fee_status.partially_paid_count + ' Students';
        document.getElementById('fee-outstanding').textContent = 'GHS ' + parseFloat(data.fee_status.outstanding_amount).toLocaleString();
        document.getElementById('fee-outstanding-count').textContent = data.fee_status.outstanding_count + ' Students';

        const tbody = document.getElementById('transactions-body');
        if (data.recent_transactions.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="text-center py-6 text-gray-400 text-xs">No transactions yet</td></tr>`;
        } else {
            tbody.innerHTML = data.recent_transactions.map(tx => `
                <tr class="border-t border-gray-50">
                    <td class="py-2.5 px-3 font-medium text-gray-700">${tx.student_name}</td>
                    <td class="py-2.5 px-3 text-gray-500">${tx.student_class}</td>
                    <td class="py-2.5 px-3 text-gray-700">GHS ${parseFloat(tx.amount).toLocaleString()}</td>
                    <td class="py-2.5 px-3">
                        <span class="px-2 py-0.5 rounded-full text-xs font-medium ${tx.status === 'Paid' ? 'bg-green-100 text-green-600' : 'bg-orange-100 text-orange-500'}">
                            ${tx.status}
                        </span>
                    </td>
                </tr>
            `).join('');
        }

        const activityList = document.getElementById('activity-list');
        if (data.recent_transactions.length === 0) {
            activityList.innerHTML = `<p class="text-xs text-gray-400 text-center py-4">No recent activity</p>`;
        } else {
            activityList.innerHTML = data.recent_transactions.slice(0, 4).map(tx => `
                <div class="flex items-start gap-3">
                    <div class="w-8 h-8 rounded-full bg-green-50 flex items-center justify-center shrink-0">
                        <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <div>
                        <p class="text-sm font-medium text-gray-700">Fee Payment</p>
                        <p class="text-xs text-gray-400">${tx.student_name} · GHS ${parseFloat(tx.amount).toLocaleString()}</p>
                        <p class="text-xs text-gray-300 mt-0.5">${tx.paid_at}</p>
                    </div>
                </div>
            `).join('');
        }

    } catch (err) {
        toast.show('Dashboard failed to load. Please refresh', 'error')
    }
}

loadDashboard();