import { component$ } from "@qwik.dev/core";
import "../style/global.css";

export default component$(() => {
    const features = [
        {
            title: "Virtual Wallet",
            description:
                "Start with $100K in virtual funds. No risk, all real.",
            icon: "💰",
        },
        {
            title: "Real-Time Data",
            description:
                "Live market prices and charts to make informed decisions.",
            icon: "📈",
        },
        {
            title: "Portfolio Tracking",
            description:
                "Track your positions, P&L, and performance over time.",
            icon: "📊",
        },
        {
            title: "Trade History",
            description: "Complete ledger of every trade you've placed.",
            icon: "📋",
        },
    ];

    const stats = [
        { value: "$100K", label: "Virtual Cash" },
        { value: "0", label: "Commission Fees" },
        { value: "Real", label: "Market Data" },
        { value: "Practice", label: "Risk Free" },
    ];

    return (
        <div>
            {/* Hero */}
            <section class="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
                    <div class="max-w-3xl mx-auto text-center">
                        <h1 class="text-4xl md:text-6xl font-bold tracking-tight mb-6">
                            Master the Market.
                            <span class="text-primary"> No Risk.</span>
                        </h1>
                        <p class="text-lg md:text-xl text-gray-300 mb-8">
                            Practice trading with virtual money. Build your
                            strategy, learn the markets, and gain confidence
                            before investing real capital.
                        </p>
                        <div class="flex flex-wrap justify-center gap-4">
                            <a
                                href="#"
                                class="inline-flex items-center px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary-dark transition-colors"
                            >
                                Start Trading Free
                            </a>
                            <a
                                href="#"
                                class="inline-flex items-center px-6 py-3 border border-gray-500 text-gray-300 font-semibold rounded-lg hover:bg-gray-800 transition-colors"
                            >
                                Learn More
                            </a>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats */}
            <section class="border-b border-gray-200 bg-white">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
                        {stats.map((stat) => (
                            <div key={stat.label} class="text-center">
                                <div class="text-3xl md:text-4xl font-bold text-gray-900">
                                    {stat.value}
                                </div>
                                <div class="text-sm text-gray-500 mt-1">
                                    {stat.label}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features */}
            <section class="py-16 md:py-24 bg-gray-50">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="text-center mb-12">
                        <h2 class="text-3xl md:text-4xl font-bold text-gray-900">
                            Everything you need to practice trading
                        </h2>
                        <p class="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
                            A complete paper trading platform designed to help
                            you learn without financial risk.
                        </p>
                    </div>
                    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {features.map((feature) => (
                            <div
                                key={feature.title}
                                class="bg-white rounded-xl p-6 border border-gray-200 hover:shadow-lg transition-shadow"
                            >
                                <div class="text-3xl mb-4">{feature.icon}</div>
                                <h3 class="text-lg font-semibold text-gray-900 mb-2">
                                    {feature.title}
                                </h3>
                                <p class="text-sm text-gray-600">
                                    {feature.description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section class="py-16 bg-white">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 class="text-3xl font-bold text-gray-900 mb-4">
                        Ready to start trading?
                    </h2>
                    <p class="text-gray-600 mb-8 max-w-xl mx-auto">
                        Create your free account and get $100K in virtual money
                        to trade with.
                    </p>
                    <a
                        href="#"
                        class="inline-flex items-center px-8 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary-dark transition-colors"
                    >
                        Create Free Account
                    </a>
                </div>
            </section>
        </div>
    );
});
