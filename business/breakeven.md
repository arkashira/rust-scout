# breakeven.md
## Unit Economics
### Cost per Active User
We estimate the following costs per active user:
* Compute: $0.05 per user per month (assuming 10,000 users, with 2 vCPUs, 4GB RAM, 30GB SSD, $50 per month)
* Storage: $0.01 per user per month (assuming 1GB storage per user, $10 per month for 1TB)
* Bandwidth: $0.005 per user per month (assuming 100MB bandwidth per user, $5 per month for 1TB)
Total cost per active user: $0.065 per user per month

## Pricing Tiers
We propose the following pricing tiers:
### Tier 1: Hobbyist
* Price: $9 per month
* Features:
	+ Access to 100 trending Rust libraries
	+ 1GB storage
	+ 100MB bandwidth
### Tier 2: Developer
* Price: $29 per month
* Features:
	+ Access to 1,000 trending Rust libraries
	+ 10GB storage
	+ 1GB bandwidth
	+ Priority support
### Tier 3: Enterprise
* Price: $99 per month
* Features:
	+ Access to all trending Rust libraries
	+ 100GB storage
	+ 10GB bandwidth
	+ Priority support
	+ Custom onboarding

## Customer Acquisition Cost (CAC) Range
Based on industry benchmarks, we estimate the CAC range to be between $10 and $50 per user.

## Lifetime Value (LTV) Estimate
Assuming an average revenue per user (ARPU) of $29 per month (Tier 2) and a customer lifetime of 12 months, we estimate the LTV to be:
LTV = ARPU x Customer Lifetime = $29 x 12 = $348

## Break-even Users Count
To calculate the break-even point, we need to consider the CAC and LTV. Assuming a CAC of $30 per user, we can calculate the break-even point as follows:
Break-even Point = CAC / (LTV - CAC) = $30 / ($348 - $30) = 0.09 or 9% of users
Break-even Users Count = Total Users x Break-even Point
Since we don't have the total users count, we will use the path to $10K MRR to estimate the break-even users count.

## Path to $10K MRR
To reach $10K MRR, we can estimate the required number of users for each tier:
* Tier 1: 1,111 users ($9 per month)
* Tier 2: 345 users ($29 per month)
* Tier 3: 101 users ($99 per month)
Assuming a mix of 20% Tier 1, 60% Tier 2, and 20% Tier 3, we can estimate the required number of users:
* Tier 1: 222 users (20% of 1,111)
* Tier 2: 207 users (60% of 345)
* Tier 3: 20 users (20% of 101)
Total users: 449 users
Break-even Users Count: 40 users (9% of 449)

Note: These estimates are based on assumptions and may vary depending on the actual market conditions and user behavior.