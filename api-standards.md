# API Design

## RESTful Patterns

- Use nouns for URLs, HTTP verbs for actions
- `GET /resources` - List resources
- `POST /resources` - Create resource
- `GET /resources/:id` - Get specific resource
- `PATCH /resources/:id` - Update resource
- `DELETE /resources/:id` - Delete resource

## Nested Resources

- `GET /users/:userId/documents` - Documents for a user
- `POST /signers/:signerId/signatures` - Create signature for signer

## Query Parameters

- Filtering: `?status=active&role=admin`
- Pagination: `?page=2&limit=20`
- Sorting: `?sort=createdAt&order=desc`

## Exceptions/Errors

- Use JSON Problem Details
